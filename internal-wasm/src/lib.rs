use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn map(mut array: Box<[u64]>) -> Box<[u64]> {
    for x in array.iter_mut() {
        *x += 1;
    }
    array
}

#[wasm_bindgen]
pub fn map_inplace(array: &mut [u64]) -> u64 {
    for x in array.iter_mut() {
        *x += 1;
    }
    array.iter().sum()
}

#[wasm_bindgen]
pub fn some_message(string: String) -> Option<String> {
    format!("your string is {:10}", string).into()
}
