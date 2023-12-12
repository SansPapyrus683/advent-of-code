const MOVE_AMT: u32 = 337;
const P1_STEPS: u32 = 2017;
const P2_STEPS: u32 = 50000000;

fn main() {
    let mut buffer = vec![0];
    let mut at = 0;
    for i in 1..=P1_STEPS {
        at = (at + MOVE_AMT as usize) % buffer.len();
        buffer.insert(at + 1, i);
        at += 1;
    }

    for i in 0..buffer.len() {
        if buffer[i] == P1_STEPS {
            println!("# after {P1_STEPS}: {}", buffer[(i + 1) % buffer.len()]);
            break;
        }
    }

    let mut at = 0;
    let mut ind1 = 0;
    for i in 1..=P2_STEPS {
        at = (at + MOVE_AMT as usize) % i as usize;
        if at + 1 == 1 {
            ind1 = i;
        }
        at += 1;
    }

    println!("index 1 after {P2_STEPS}: {ind1}");
}
