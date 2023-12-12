const KEY: &str = "yzbqklnj";
const P1_ZEROS: u32 = 5;
const P2_ZEROS: u32 = 6;

fn zero_start_amt(s: &str) -> u32 {
    for (i, c) in s.bytes().enumerate() {
        if c as char != '0' {
            return i as u32;
        }
    }
    return s.len() as u32;
}

fn main() {
    let mut at = 0;
    let mut found = (false, false);
    loop {
        let hsh = KEY.to_owned() + &at.to_string();
        let digest = format!("{:x}", md5::compute(hsh));
        let zero_amt = zero_start_amt(&digest);

        if zero_amt >= P1_ZEROS && !found.0 {
            println!("first index with {P1_ZEROS} 0s at start: {at}");
            found.0 = true;
        }
        if zero_amt >= P2_ZEROS && !found.1 {
            println!("first index with {P2_ZEROS} 0s at start: {at}");
            found.1 = true;
        }

        if found.0 && found.1 {
            break;
        }
        at += 1;
    }
}
