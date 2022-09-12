use std::collections::HashMap;

const STEPS: u32 = 12302209;
const START: State = State::A;

struct Action { write: bool, shift: i32, next: State }
struct StateExec { zero: Action, one: Action }
enum State { A, B, C, D, E, F }

impl State {
    fn to_exec(&self) -> StateExec {
        // you're on your own if you wanna use this for your own input
        match self {
            State::A => StateExec {
                zero: Action { write: true, shift: 1, next: Self::B },
                one: Action { write: false, shift: -1, next: Self::D }
            },
            State::B => StateExec {
                zero: Action { write: true, shift: 1, next: Self::C },
                one: Action { write: false, shift: 1, next: Self::F }
            },
            State::C => StateExec {
                zero: Action { write: true, shift: -1, next: Self::C },
                one: Action { write: true, shift: -1, next: Self::A }
            },
            State::D => StateExec {
                zero: Action { write: false, shift: -1, next: Self::E },
                one: Action { write: true, shift: 1, next: Self::A }
            },
            State::E => StateExec {
                zero: Action { write: true, shift: -1, next: Self::A },
                one: Action { write: false, shift: 1, next: Self::B }
            },
            State::F => StateExec {
                zero: Action { write: false, shift: 1, next: Self::C },
                one: Action { write: false, shift: 1, next: Self::E }
            },
        }
    }

    fn exec(&self, tape: &mut HashMap<i32, bool>, at: &mut i32) -> Self {
        let curr = tape.entry(*at).or_default();
        let action = self.to_exec();
        let action = if *curr { action.one } else { action.zero };
        *curr = action.write;
        *at += action.shift;
        action.next
    }
}

fn main() {
    let mut tape = HashMap::new();
    let mut state = START;
    let mut at = 0;
    for _ in 0..STEPS {
        state = state.exec(&mut tape, &mut at);
    }

    let sum = tape.values().fold(0, |acc, &b| acc + if b { 1 } else { 0 });
    println!("final checksum after {STEPS} steps: {sum}");
}
