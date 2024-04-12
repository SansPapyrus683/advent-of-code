use std::collections::VecDeque;

const SCORE_INTERVAL: u32 = 23;
const CC_REMOVED: u32 = 7;

const PLAYERS: u32 = 413;
const LAST_VAL: u32 = 71082;

fn scores(player_num: u32, last_marble_score: u32) -> Vec<u32> {
    let mut ret = vec![0; player_num as usize];
    let mut circle: VecDeque<u32> = VecDeque::from([0]);
    for m in 1..last_marble_score {
        if m % SCORE_INTERVAL == 0 {
            let player = (m - 1) % player_num;
            ret[player as usize] += m;
            for _ in 0..CC_REMOVED {
                let tmp = circle.pop_back().unwrap();
                circle.push_front(tmp);
            }
            ret[player as usize] += &circle.pop_front().unwrap();
        } else {
            for _ in 0..2 {
                let tmp = circle.pop_front().unwrap();
                circle.push_back(tmp);
            }
            circle.push_front(m);
        }
    }
    ret
}

fn main() {
    println!(
        "winning score (p1): {}",
        scores(PLAYERS, LAST_VAL).iter().max().unwrap()
    );
    println!(
        "winning score (p2): {}",
        scores(PLAYERS, LAST_VAL * 100).iter().max().unwrap()
    );
}
