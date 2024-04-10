use std::fs;

fn main() {
    let sheet = fs::read_to_string("../input/day2.txt").expect("bruh");

    let mut checksum = 0;
    let mut res_sum = 0;
    for row in sheet.lines() {
        let nums: Vec<i32> = row.split_whitespace()
            .map(|n| n.parse::<i32>().unwrap_or(0))
            .collect();

        checksum += nums.iter().max().unwrap_or(&0) - nums.iter().min().unwrap_or(&0);

        'search:
        for i in 0..nums.len() {
            for j in i + 1..nums.len() {
                if nums[i] % nums[j] == 0 {
                    res_sum += nums[i] / nums[j];
                    break 'search;
                }
                if nums[j] % nums[i] == 0 {
                    res_sum += nums[j] / nums[i];
                    break 'search;
                }
            }
        }
    }

    dbg!(checksum);
    dbg!(res_sum);
}
