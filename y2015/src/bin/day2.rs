use std::fs;

#[derive(Debug)]
struct Gift { l: u32, w: u32, h: u32 }

impl Gift {
    fn longest_side(&self) -> u32 {
        self.l.max(self.w.max(self.h))
    }

    fn vol(&self) -> u32 { self.l * self.w * self.h }

    fn surface_area(&self) -> u32 {
        2 * (self.l * self.w + self.w * self.h + self.l * self.h)
    }

    fn smallest_perim(&self) -> u32 {
        2 * (self.l + self.w + self.h - self.longest_side())
    }
}

fn main() {
    let read = fs::read_to_string("input/day2.txt").expect("you done messed up");
    let lines: Vec<&str> = read.split_whitespace().collect();

    let gift_fmt = regex::Regex::new(r"(\d+)x(\d+)x(\d+)").unwrap();
    let mut gifts: Vec<Gift> = Vec::new();
    for l in &lines {
        for d in gift_fmt.captures_iter(l) {
             gifts.push(Gift{
                l: d[1].parse().unwrap(),
                w: d[2].parse().unwrap(),
                h: d[3].parse().unwrap(),
            });
        }
    }

    let mut wrapping_paper = 0;
    let mut ribbon = 0;
    for g in &gifts {
        wrapping_paper += g.surface_area() + g.vol() / g.longest_side();
        ribbon += g.smallest_perim() + g.vol()
    }

    println!("wrapping paper amt: {wrapping_paper}");
    println!("ribbon amt: {ribbon}");
}
