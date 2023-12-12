use std::fs;
use regex::Regex;

const TOTAL: i64 = 100;
const MEAL_CAL_AMT: i64 = 500;

struct Ingredient {
    cap: i64,
    durability: i64,
    flavor: i64,
    texture: i64,
    cal: i64
}

fn main() {
    // really sorry for the long regex
    let ing_fmt = Regex::new(
        r"[a-z]*: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    ).unwrap();

    let read = fs::read_to_string("../input/day15.txt").expect("bruh");

    let mut ings = Vec::new();
    for i in read.lines() {
        if let Some(m) = ing_fmt.captures(i) {
            ings.push(Ingredient {
                cap: m[1].parse().unwrap(),
                durability: m[2].parse().unwrap(),
                flavor: m[3].parse().unwrap(),
                texture: m[4].parse().unwrap(),
                cal: m[5].parse().unwrap()
            });
        }
    }

    let mut configs = vec![Vec::new()];
    for i in 0..ings.len() {
        let mut new_configs = Vec::new();
        for c in configs {
            let curr_total: i64 = c.iter().sum();
            if i == ings.len() - 1 {
                let mut new_c = c.clone();
                new_c.push(TOTAL - curr_total);
                new_configs.push(new_c);
                continue;
            }
            for n in 1..=(TOTAL - curr_total) {
                let mut new_c = c.clone();
                new_c.push(n);
                new_configs.push(new_c);
            }
        }
        configs = new_configs;
    }

    let mut hi_score = i64::MIN;
    let mut meal_score = i64::MIN;
    for cfg in configs {
        let mut c = Ingredient {
            cap: 0, durability: 0, flavor: 0, texture: 0, cal: 0
        };
        for (i, amt) in ings.iter().zip(&cfg) {
            c.cap += i.cap * amt;
            c.durability += i.durability * amt;
            c.flavor += i.flavor * amt;
            c.texture += i.texture * amt;
            c.cal += i.cal * amt;
        }

        let score =
            c.cap.max(0)
            * c.durability.max(0)
            * c.flavor.max(0)
            * c.texture.max(0);

        hi_score = hi_score.max(score);
        if c.cal == MEAL_CAL_AMT {
            meal_score = meal_score.max(score);
        }
    }

    println!("highest score cookie: {hi_score}");
    println!("highest score with {MEAL_CAL_AMT} calories: {meal_score}");
}
