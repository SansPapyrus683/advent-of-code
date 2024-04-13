const FIRST: u8 = 3;
const SECOND: u8 = 7;
const TARGET: u32 = 556061;
const P1_TAKE: u32 = 10;

fn main() {
    let target_len = TARGET.to_string().len();

    let mut sb = vec![FIRST, SECOND];
    let mut p1_sat = false;
    let mut p2_sat = false;
    let mut elf1 = 0;
    let mut elf2 = 1;
    while !p1_sat || !p2_sat {
        let recipe = sb[elf1] + sb[elf2];
        sb.append(&mut recipe.to_string().chars().map(|c| c as u8 - b'0').collect());

        elf1 = (elf1 + sb[elf1] as usize + 1) % sb.len();
        elf2 = (elf2 + sb[elf2] as usize + 1) % sb.len();

        if sb.len() >= (TARGET + P1_TAKE) as usize && !p1_sat {
            print!("the scores of the {P1_TAKE} recipes after: ");
            for i in (sb.len() - P1_TAKE as usize)..sb.len() {
                print!("{}", sb[i]);
            }
            println!();
            p1_sat = true;
        }

        if sb.len() >= target_len && !p2_sat {
            for offset in 0..=1.min(sb.len() - target_len) {
                let mut last_digits = 0;
                for i in (sb.len() - target_len - offset)..(sb.len() - offset) {
                    last_digits = last_digits * 10 + sb[i] as u32;
                }

                if last_digits == TARGET {
                    println!(
                        "number of runs to get the sequence: {}",
                        sb.len() - target_len - offset
                    );
                    p2_sat = true;
                    break;
                }
            }
        }
    }
}
