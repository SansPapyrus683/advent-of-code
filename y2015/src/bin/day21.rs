use std::ops;
use itertools::Itertools;

#[derive(Clone, Copy)] struct Entity { hp: i32, atk: i32, def: i32 }
#[derive(Clone)] struct Thing { cost: i32, dmg: i32, def: i32 }

// can't believe i have to do this it's so cancer
impl ops::Add for Thing {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Thing {
            cost: self.cost + other.cost,
            dmg: self.dmg + other.dmg,
            def: self.def + other.def
        }
    }
}

impl<'a, 'b> ops::Add<&'b Thing> for &'a Thing {
    type Output = Thing;
    fn add(self, other: &'b Thing) -> Thing {
        Thing {
            cost: self.cost + other.cost,
            dmg: self.dmg + other.dmg,
            def: self.def + other.def
        }
    }
}

// bro this is absolute cancer
const WEAPONS: [Thing; 5] = [
    Thing { cost: 8, dmg: 4, def: 0 },
    Thing { cost: 10, dmg: 5, def: 0 },
    Thing { cost: 25, dmg: 6, def: 0 },
    Thing { cost: 40, dmg: 7, def: 0 },
    Thing { cost: 74, dmg: 8, def: 0 }
];
const ARMOR: [Thing; 5] = [
    Thing { cost: 13, dmg: 0, def: 1 },
    Thing { cost: 31, dmg: 0, def: 2 },
    Thing { cost: 53, dmg: 0, def: 3 },
    Thing { cost: 75, dmg: 0, def: 4 },
    Thing { cost: 102, dmg: 0, def: 5 }
];
const RINGS: [Thing; 6] = [
    Thing { cost: 25, dmg: 1, def: 0 },
    Thing { cost: 50, dmg: 2, def: 0 },
    Thing { cost: 100, dmg: 3, def: 0 },
    Thing { cost: 20, dmg: 0, def: 1 },
    Thing { cost: 40, dmg: 0, def: 2 },
    Thing { cost: 80, dmg: 0, def: 3 }
];
const NOTHING: Thing = Thing { cost: 0, dmg: 0, def: 0 };

fn atk(a: &mut Entity, d: &mut Entity) {
    let dmg = if a.atk > d.def { a.atk - d.def } else { 1 };
    d.hp -= dmg;
}

fn can_beat(me: &Entity, other: &Entity) -> bool {
    let mut mme = me.clone();
    let mut oother = other.clone();
    let mut turn = true;  // true = me, false = enemy
    while mme.hp > 0 && oother.hp > 0 {
        if turn {
            atk(&mut mme, &mut oother);
        } else {
            atk(&mut oother, &mut mme);
        }
        turn = !turn;
    }
    mme.hp > 0
}

fn main() {
    let boss = Entity { hp: 104, atk: 8, def: 1 };
    let my_hp = 100;

    let mut armor_combs = ARMOR.to_vec();
    armor_combs.push(NOTHING);

    let mut ring_combs = vec![vec![NOTHING]];
    for i in 1..=2 {
        for comb in RINGS.into_iter().combinations(i) {
            ring_combs.push(comb);
        }
    }

    let mut gear_combs = Vec::new();
    for w in &WEAPONS {
        for a in &armor_combs {
            for rc in &ring_combs {
                let mut total = w + a;
                for r in rc {
                    total = &total + r;
                }
                gear_combs.push(total);
            }
        }
    }

    let mut min_win = i32::MAX;
    let mut max_lose = i32::MIN;
    for gc in gear_combs {
        let me = Entity {
            hp: my_hp,
            atk: gc.dmg,
            def: gc.def
        };
        if can_beat(&me, &boss) {
            min_win = min_win.min(gc.cost);
        } else {
            max_lose = max_lose.max(gc.cost);
        }
    }

    println!("min gold to win: {min_win}");
    println!("max gold to (still) lose: {max_lose}");
}
