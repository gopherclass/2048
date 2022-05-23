import * as wasm from "internal-wasm";
import * as onnx from "onnx";

import Actuator from "./html_actuator.js";
import GameManager from "./game_manager.js"
import HTMLActuator from "./html_actuator.js";
import InputManager from "./keyboard_input_manager.js";
import KeyboardInputManager from "./keyboard_input_manager.js";
import LocalStorageManager from "./local_storage_manager.js";

function encodeToTensor(state) {
  const input = new Float32Array(16 * 4 * 4);
  for (let j = 0; j < 16; j++) {
    input[j] = state[j] == 0 ? 1 : 0;
  }
  for (let i = 1; i < 16; i++) {
    for (let j = 0; j < 16; j++) {
      input[i * 16 + j] = state[j] === (1 << i) ? 1 : 0;
    }
  }
  return new onnx.Tensor(input, "float32", [1, 16, 4, 4]);
};

function argmax(array) {
  if (array.length === 0) {
    return undefined;
  }
  let arg = 0;
  let max = array[0];
  for (let i = 1; i < array.length; i++) {
    if (max < array[i]) {
      arg = i;
      max = array[i]
    }
  }
  return arg;
}

window.requestAnimationFrame(async () => {
  const game = new GameManager(4, KeyboardInputManager, HTMLActuator, LocalStorageManager);
  const source = new wasm.PCGSource(1n, 0n);

  const runMC = () => {
    const dir = wasm.walk(game.grid.typedArray(), source);
    game.move(dir);
  };
  const runCNN = async () => {
    const outputMap = await sess.run([encodeToTensor(game.grid.typedArray())]);
    const outputTensor = outputMap.values().next().value;
    const predictions = outputTensor.data;
    for (let i = 0; i < 4; i++) {
      if (!game.moveAvailable(i)) {
        predictions[i] = Number.NEGATIVE_INFINITY;
      }
    }
    const dir = argmax(predictions);
    game.move(dir);
  };

  let currentAlgorithm = undefined;
  const runAlg = async () => {
    if (currentAlgorithm !== undefined) {
      await currentAlgorithm();
      setTimeout(window.requestAnimationFrame, 100, runAlg);
    }
  };

  document.getElementById("run-mc").addEventListener("click", (event) => {
    event.preventDefault();
    if (currentAlgorithm === undefined) {
      runMC();
    }
  });

  document.getElementById("run-mc").addEventListener("contextmenu", (event) => {
    event.preventDefault();
    if (currentAlgorithm === undefined) {
      currentAlgorithm = runMC;
      window.requestAnimationFrame(runAlg);
    } else {
      currentAlgorithm = undefined;
    }
  });

  const sess = new onnx.InferenceSession();
  await sess.loadModel("./model.onnx");

  document.getElementById("run-cnn").addEventListener("click", (event) => {
    event.preventDefault();
    if (currentAlgorithm === undefined) {
      runCNN();
    }
  });
  document.getElementById("run-cnn").addEventListener("contextmenu", (event) => {
    event.preventDefault();
    if (currentAlgorithm === undefined) {
      currentAlgorithm = runCNN;
      window.requestAnimationFrame(runAlg);
    } else {
      currentAlgorithm = undefined;
    }
  });
});

