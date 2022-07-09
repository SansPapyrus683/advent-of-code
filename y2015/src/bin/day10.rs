const INIT_SEQ: &str = "1113122113";
const P1_AMT: u32 = 40;
const P2_AMT: u32 = 50;

fn main() {
    let mut char_seq: Vec<char> = INIT_SEQ.chars().into_iter().collect();

    let mut seq = Vec::new();
    for c in char_seq {
        seq.push(c.to_digit(10).unwrap());
    }

    for i in 1..=P1_AMT.max(P2_AMT) {
        let mut new_seq = Vec::new();
        let mut prev = 0;  // initial value won't be used
        let mut prev_len = 0;
        let mut first_time = true;
        for i in seq {
            if first_time {
                prev = i;
                first_time = false;
            }
            if i != prev {
                new_seq.extend([prev_len, prev]);
                prev_len = 0;
                prev = i;
            }
            prev_len += 1;
        }
        new_seq.extend([prev_len, prev]);
        seq = new_seq;

        if i == P1_AMT {
            println!("result len after {P1_AMT} steps: {}", seq.len());
        }
        if i == P2_AMT {
            println!("result len after {P2_AMT} steps: {}", seq.len());
        }
    }
}
