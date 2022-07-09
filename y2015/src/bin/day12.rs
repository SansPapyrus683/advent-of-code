use std::fs;
use serde_json::Value;

fn num_sum(val: &Value, invalid: &Option<&Vec<String>>) -> i64 {
    let mut total = 0;
    if val.is_array() {
        for v in val.as_array().unwrap() {
            if v.is_number() {
                total += v.as_i64().unwrap();
            } else if v.is_array() || v.is_object() {
                total += num_sum(v, invalid);
            }
        }
    } else if val.is_object() {
        for (_, v) in val.as_object().unwrap() {
            if v.is_string() && invalid.is_some()
                && invalid.unwrap().contains(&v.as_str().unwrap().to_string()) {
                return 0;
            }
            if v.is_number() {
                total += v.as_i64().unwrap();
            } else if v.is_array() || v.is_object() {
                total += num_sum(v, invalid);
            }
        }
    }
    total
}

fn main() {
    let raw_json = fs::read_to_string("input/day12.txt").expect("you done messed up");
    let json: Value = serde_json::from_str(&raw_json).expect("bad json");

    println!("raw sum of #s: {}", num_sum(&json, &None));

    let invalid = vec!["red".to_string()];
    println!("sum of #s w/ the red restriction: {}", num_sum(&json, &Some(&invalid)));
}
