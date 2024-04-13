use regex::Regex;
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::fs;

const WORKER_NUM: u32 = 5;

fn main() {
    let order_fmt =
        Regex::new("Step ([A-Z]) must be finished before step ([A-Z]) can begin").unwrap();
    let mut prereqs = HashMap::new();
    let mut fulfills = HashMap::new();
    let mut all_tasks = HashSet::new();
    for req in fs::read_to_string("../input/day7.txt").unwrap().lines() {
        if let Some(m) = order_fmt.captures(req) {
            let a = m[1].chars().nth(0).unwrap();
            let b = m[2].chars().nth(0).unwrap();
            all_tasks.insert(a);
            all_tasks.insert(b);

            if !prereqs.contains_key(&b) {
                prereqs.insert(b, Vec::new());
            }
            prereqs.get_mut(&b).unwrap().push(a);
            if !fulfills.contains_key(&a) {
                fulfills.insert(a, Vec::new());
            }
            fulfills.get_mut(&a).unwrap().push(b);
        }
    }

    let mut unfinished_num = HashMap::new();
    let no_prereqs = all_tasks
        .iter()
        .filter(|t| !prereqs.contains_key(t))
        .map(|t| Reverse(*t))
        .collect::<Vec<_>>();

    prereqs.iter().for_each(|(task, pre)| {
        unfinished_num.insert(task, pre.len());
    });
    let mut can_do: BinaryHeap<_> = BinaryHeap::from(no_prereqs.clone());
    let mut order = Vec::new();
    while !can_do.is_empty() {
        let curr = can_do.pop().unwrap().0;
        order.push(curr);
        for p in fulfills.get(&curr).unwrap_or(&Vec::new()) {
            *unfinished_num.get_mut(&p.clone()).unwrap() -= 1;
            if unfinished_num[&p] == 0 {
                can_do.push(Reverse(*p));
            }
        }
    }

    println!("task order: {}", String::from_iter(order));

    // ik doing two toposorts is pretty dumb but hey it works
    prereqs.iter().for_each(|(task, pre)| {
        unfinished_num.insert(task, pre.len());
    });
    can_do = BinaryHeap::from(no_prereqs.clone());
    let mut elves = vec![None; WORKER_NUM as usize];
    let mut done = Vec::new();
    let mut time = 0;
    while done.len() < all_tasks.len() {
        let mut to_add = Vec::new();
        for w in 0..WORKER_NUM {
            let e = elves.get_mut(w as usize).unwrap();
            if e.is_none() && !can_do.is_empty() {
                let todo = can_do.pop().unwrap().0;
                *e = Some((todo, 60 + todo as u32 - 'A' as u32 + 1));
            }
            if e.is_some() {
                let elf = e.as_mut().unwrap();
                elf.1 -= 1;
                if elf.1 == 0 {
                    done.push(elf.0);
                    for p in fulfills.get(&elf.0).unwrap_or(&Vec::new()) {
                        *unfinished_num.get_mut(&p.clone()).unwrap() -= 1;
                        if unfinished_num[&p] == 0 {
                            to_add.push(Reverse(*p));
                        }
                    }
                    *e = None;
                }
            }
        }
        to_add.iter().for_each(|t| can_do.push(*t));
        time += 1;
    }

    println!("min time to finish all tasks: {time}");
}
