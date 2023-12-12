use std::fs;

fn decode_len(s: &str) -> Result<i32, &str> {
    let mut chars = s.as_bytes();
    if chars[0] != '"' as u8 || chars[s.len() - 1] != '"' as u8 {
        return Err("bro wth");
    }

    let string = &s[1..s.len() - 1];
    let mut at = 0;
    let mut len = 0;
    let chars = string.as_bytes();
    while at < string.len() {
        let c = chars[at] as char;
        if c == '\\' {
            let nxt = chars[at + 1] as char;
            if nxt == 'x' {
                at += 4;
            } else if nxt == '"' || nxt == '\\' {
                at += 2;
            } else {
                return Err("bro wth");
            }
        } else {
            at += 1;
        }
        len += 1;
    }
    Ok(len)
}

fn encode_len(s: &str) -> i32 {
    s.len() as i32 + s.matches('"').count() as i32 + s.matches('\\').count() as i32 + 2
}

fn main() {
    let read = fs::read_to_string("input/day8.txt").expect("bruh");

    let mut total_og_len = 0;
    let mut total_decode_len = 0;
    let mut total_encode_len = 0;
    for s in read.lines() {
        total_og_len += s.len() as i32;
        total_decode_len += decode_len(&s).unwrap();
        total_encode_len += encode_len(&s);
    }

    println!("og - decode len: {}", total_og_len - total_decode_len);
    println!("encode - og len: {}", total_encode_len - total_og_len);
}
