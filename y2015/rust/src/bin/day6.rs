use std::fs;
use regex::Regex;

const DIMS: (usize, usize) = (1000, 1000);

struct Pt { r: usize, c: usize }
enum IId { On, Off, Toggle }
struct Instruction { i_type: IId, start: Pt, end: Pt }

impl Instruction {
    fn binary_exe(&self, lights: &mut Vec<Vec<bool>>) {
        for r in self.start.r..=self.end.r {
            for c in self.start.c..=self.end.c {
                match self.i_type {
                    IId::On => lights[r][c] = true,
                    IId::Off => lights[r][c] = false,
                    IId::Toggle => lights[r][c] = !lights[r][c]
                }
            }
        }
    }

    fn brightness_exe(&self, lights: &mut Vec<Vec<u32>>) {
        for r in self.start.r..=self.end.r {
            for c in self.start.c..=self.end.c {
                match self.i_type {
                    IId::On => lights[r][c] += 1,
                    IId::Off => {
                        if lights[r][c] > 0 {
                            lights[r][c] -= 1;
                        }
                    }
                    IId::Toggle => lights[r][c] += 2
                }
            }
        }
    }
}

fn main() {
    // sorry for the long regexes
    let on_fmt = Regex::new(r"turn on (\d+),(\d+) through (\d+),(\d+)").unwrap();
    let off_fmt = Regex::new(r"turn off (\d+),(\d+) through (\d+),(\d+)").unwrap();
    let toggle_fmt = Regex::new(r"toggle (\d+),(\d+) through (\d+),(\d+)").unwrap();

    let read = fs::read_to_string("../input/day6.txt").expect("bruh");
    let mut instructions = Vec::new();
    for i in read.lines() {
        let mut to_use = None;
        let mut i_type = None;
        if on_fmt.is_match(i) {
            i_type = Some(IId::On);
            to_use = Some(&on_fmt);
        } else if off_fmt.is_match(i) {
            i_type = Some(IId::Off);
            to_use = Some(&off_fmt);
        } else if toggle_fmt.is_match(i) {
            i_type = Some(IId::Toggle);
            to_use = Some(&toggle_fmt);
        }

        let p = to_use.unwrap().captures(i).unwrap();
        instructions.push(Instruction {
            i_type: i_type.unwrap(),
            start: Pt { r: p[1].parse().unwrap(), c: p[2].parse().unwrap() },
            end: Pt { r: p[3].parse().unwrap(), c: p[4].parse().unwrap() },
        });
    }

    let mut lights1 = vec![vec![false; DIMS.1]; DIMS.0];
    let mut lights2 = vec![vec![0; DIMS.1]; DIMS.0];
    for i in &instructions {
        i.binary_exe(&mut lights1);
        i.brightness_exe(&mut lights2);
    }

    let mut total1: u32 = 0;
    let mut total2: u32 = 0;
    for r in 0..DIMS.0 {
        for c in 0..DIMS.1 {
            total1 += lights1[r][c] as u32;
            total2 += lights2[r][c];
        }
    }

    println!("p1 total brightness: {total1}");
    println!("p2 total brightness: {total2}");
}
