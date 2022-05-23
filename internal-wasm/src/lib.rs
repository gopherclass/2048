use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn walk(buf: &[u32], source: &mut PCGSource) -> Option<u8> {
    let x = from_state_buf(buf)?;
    if let Some((kind, _, _)) = mc(x, 100, source) {
        Some(kind as u8)
    } else {
        None
    }
}

fn place(state: &mut State, src: &mut PCGSource) -> bool {
    let (mut avails, mut n) = ([0; 16], 0);
    for (i, at) in state.iter().enumerate() {
        if *at == 0 {
            avails[n] = i;
            n += 1;
        }
    }
    let i = src.choice(avails[..n].as_ref()).copied();
    if let Some(i) = i {
        state[i] = if src.bernoulli(1, 10) { 2 } else { 1 };
    }
    i.is_some()
}

fn mc(state: State, pop: usize, src: &mut PCGSource) -> Option<(Dir, State, u32)> {
    let mut maxexp = 0.0;
    let mut arg = None;
    for kind in [Dir::L, Dir::R, Dir::U, Dir::D] {
        step_if(state, kind, |kind, new_state, n| {
            let exp = n as f64 + exp(new_state, pop, src);
            if maxexp < exp {
                maxexp = exp;
                arg = Some((kind, new_state, n));
            }
        });
    }
    arg
}

fn exp(x0: State, pop: usize, src: &mut PCGSource) -> f64 {
    let mut pay = 0;
    let mut branches = Vec::with_capacity(4);
    for _ in 0..pop {
        let mut x = x0;
        for _ in 0..100 {
            branches.clear();
            let mut pred = |_, y, n| {
                branches.push((y, n));
            };
            step_if(x, Dir::L, &mut pred);
            step_if(x, Dir::R, &mut pred);
            step_if(x, Dir::U, &mut pred);
            step_if(x, Dir::D, &mut pred);
            if branches.len() == 0 {
                break;
            }
            let i = src.res(branches.len() as u64) as usize;
            let (ref y, ref n) = branches[i];
            x = *y;
            pay += *n;
            place(&mut x, src);
        }
    }
    (pay as f64) / (pop as f64)
}

fn display(x: State) {
    println!("{:?}", &x[0..4]);
    println!("{:?}", &x[4..8]);
    println!("{:?}", &x[8..12]);
    println!("{:?}", &x[12..16]);
}

#[derive(Clone, Copy, Debug)]
#[repr(u8)]
enum Dir {
    U = 0,
    R = 1,
    D = 2,
    L = 3,
}

type State = [u32; 16];

fn from_state_buf(buf: &[u32]) -> Option<State> {
    if buf.len() != 16 {
        return None;
    }
    let mut state = [0; 16];
    for i in 0..16 {
        state[i] = buf[i];
    }
    Some(state)
}

#[inline]
fn step_if<F>(x: State, kind: Dir, mut pred: F) -> bool
where
    F: FnMut(Dir, State, u32),
{
    let (y, n, tr) = step(x, kind);
    if tr {
        pred(kind, y, n);
    }
    tr
}

fn step(mut x: State, kind: Dir) -> (State, u32, bool) {
    let mut n = 0;
    let mut tr = false;
    match kind {
        Dir::L => {
            merge(&mut x, &mut n, &mut tr, |i| i);
            merge(&mut x, &mut n, &mut tr, |i| 4 + i);
            merge(&mut x, &mut n, &mut tr, |i| 8 + i);
            merge(&mut x, &mut n, &mut tr, |i| 12 + i);
        }
        Dir::R => {
            merge(&mut x, &mut n, &mut tr, |i| 3 - i);
            merge(&mut x, &mut n, &mut tr, |i| 7 - i);
            merge(&mut x, &mut n, &mut tr, |i| 11 - i);
            merge(&mut x, &mut n, &mut tr, |i| 15 - i);
        }
        Dir::D => {
            merge(&mut x, &mut n, &mut tr, |i| 4 * (3 - i));
            merge(&mut x, &mut n, &mut tr, |i| 4 * (3 - i) + 1);
            merge(&mut x, &mut n, &mut tr, |i| 4 * (3 - i) + 2);
            merge(&mut x, &mut n, &mut tr, |i| 4 * (3 - i) + 3);
        }
        Dir::U => {
            merge(&mut x, &mut n, &mut tr, |i| 4 * i);
            merge(&mut x, &mut n, &mut tr, |i| 4 * i + 1);
            merge(&mut x, &mut n, &mut tr, |i| 4 * i + 2);
            merge(&mut x, &mut n, &mut tr, |i| 4 * i + 3);
        }
    };
    (x, n, tr)
}

fn merge<F>(v: &mut State, n: &mut u32, tr: &mut bool, ind: F)
where
    F: Fn(usize) -> usize,
{
    let mut i = 0;
    let mut j = 1;
    while j < 4 {
        if i >= j {
            j += 1;
        } else if v[ind(i)] == 0 && v[ind(j)] == 0 {
            j += 1;
        } else if v[ind(i)] == 0 {
            *tr = true;
            v[ind(i)] = v[ind(j)];
            v[ind(j)] = 0;
            j += 1;
        } else if v[ind(j)] == 0 {
            j += 1;
        } else if v[ind(i)] == v[ind(j)] {
            *tr = true;
            *n += 2 << v[ind(i)];
            v[ind(i)] += 1;
            v[ind(j)] = 0;
            i += 1;
            j += 1;
        } else {
            i += 1;
        }
    }
}

#[wasm_bindgen]
pub struct PCGSource {
    state: u128,
}

#[wasm_bindgen]
impl PCGSource {
    #[wasm_bindgen(constructor)]
    pub fn constructor(lo: u64, hi: u64) -> Self {
        Self {
            state: ((hi as u128) << 64) | (lo as u128),
        }
    }
}

impl PCGSource {
    fn u64(&mut self) -> u64 {
        const PCG_DEFAULT_MULTIPLIER_128: u128 = 0x2360ed051fc65da44385df649fccf645;
        const PCG_DEFAULT_INCREMENT_128: u128 = 0x5851f42d4c957f2d14057b7ef767814f;

        self.state = self
            .state
            .wrapping_mul(PCG_DEFAULT_MULTIPLIER_128)
            .wrapping_add(PCG_DEFAULT_INCREMENT_128);
        ((self.state as u64) ^ ((self.state >> 64) as u64)).rotate_right((self.state >> 122) as u32)
    }

    fn u128(&mut self) -> u128 {
        ((self.u64() as u128) << 64) | (self.u64() as u128)
    }

    fn res(&mut self, n: u64) -> u64 {
        if n.is_power_of_two() {
            self.u64() & (n - 1)
        } else {
            let reject = u64::MAX - u64::MAX % n;
            let mut v = self.u64();
            while v > reject {
                v = self.u64();
            }
            v % n
        }
    }

    fn choice<'a, T>(&mut self, v: &'a [T]) -> Option<&'a T> {
        if v.len() > 0 {
            let i = self.res(v.len() as u64) as usize;
            v.get(i)
        } else {
            None
        }
    }

    fn bernoulli(&mut self, m: u64, n: u64) -> bool {
        self.res(n) < m
    }
}
