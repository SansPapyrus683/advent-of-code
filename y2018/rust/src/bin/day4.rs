use std::collections::HashMap;
use std::fs;

use chrono::{Duration, NaiveDateTime, Timelike};
use regex::Regex;

#[derive(Debug)]
enum Event {
    Sleep,
    Wake,
    Begin(u32),
}

fn main() {
    let event_fmt = Regex::new(r"\[(.*)] (.*)").unwrap();
    let guard_fmt = Regex::new(r"guard #(\d+) begins shift").unwrap();
    let mut events: Vec<(NaiveDateTime, Event)> = fs::read_to_string("../input/day4.txt")
        .unwrap()
        .lines()
        .map(|e| {
            let raw = event_fmt.captures(e).unwrap();
            let time = NaiveDateTime::parse_from_str(&raw[1], "%Y-%m-%d %H:%M").unwrap();
            let what = &raw[2].to_lowercase();
            return (
                time,
                if what == "wakes up" {
                    Event::Wake
                } else if what == "falls asleep" {
                    Event::Sleep
                } else {
                    let guard_id = guard_fmt.captures(what).unwrap()[1].parse::<u32>().unwrap();
                    Event::Begin(guard_id)
                },
            );
        })
        .collect();

    events.sort_by(|a, b| a.0.cmp(&b.0));

    let mut minutes_slept: HashMap<u32, HashMap<u32, u32>> = HashMap::new();
    let mut curr_guard = u32::MAX;
    let mut last_time = None;
    for (t, e) in &events {
        match e {
            Event::Sleep => {
                last_time = Some(*t);
            }
            Event::Wake => {
                let mut curr_at = last_time.unwrap();
                assert_ne!(curr_guard, u32::MAX);
                if !minutes_slept.contains_key(&curr_guard) {
                    minutes_slept.insert(curr_guard, HashMap::new());
                }
                while curr_at < *t {
                    minutes_slept
                        .get_mut(&curr_guard)
                        .unwrap()
                        .entry(curr_at.minute())
                        .and_mshouldodify(|freq| *freq += 1)
                        .or_insert(1);
                    curr_at += Duration::minutes(1);
                }
            }
            Event::Begin(id) => {
                curr_guard = *id;
            }
        }
    }

    let guard_prod =
        |(g, m): (&u32, &HashMap<u32, u32>)| g * m.iter().max_by_key(|i| i.1).unwrap().0;

    let strat1 = minutes_slept
        .iter()
        .max_by(|(_, m1), (_, m2)| m1.values().sum::<u32>().cmp(&m2.values().sum::<u32>()))
        .map(guard_prod)
        .unwrap();

    println!("result of strategy 1: {strat1}");

    let strat2 = minutes_slept
        .iter()
        .max_by(|(_, m1), (_, m2)| m1.values().max().cmp(&m2.values().max()))
        .map(guard_prod)
        .unwrap();

    println!("result of strategy 2: {strat2}");
}
