/// sorry for the spaghetti code

use strum::IntoEnumIterator;
use strum_macros::EnumIter;

const BOSS_HP: i32 = 71;
const BOSS_ATK: i32 = 10;

#[derive(Debug, Copy, Clone, EnumIter)]
enum Spell { Missile, Drain, Shield, Recharge, Poison }
impl Spell {
    fn cost(&self) -> i32 {
        match self {
            Spell::Missile => 53,
            Spell::Drain => 73,
            Spell::Shield => 113,
            Spell::Recharge => 229,
            Spell::Poison => 173
        }
    }

    fn effect(&self) -> Option<Effect> {
        match self {
            Spell::Missile => None,
            Spell::Drain => None,
            Spell::Shield => Some(Effect::Shield),
            Spell::Recharge => Some(Effect::Recharge),
            Spell::Poison => Some(Effect::Poison)
        }
    }
}

#[derive(Debug, Copy, Clone, PartialEq)]
enum Effect { Shield, Poison, Recharge }
#[derive(Debug, PartialEq)]
enum Status { Win, Loss, Undecided }

#[derive(Debug, Clone)]
struct Game {
    p_effects: Vec<(Effect, i32)>,
    p_hp: i32, p_mana: i32, p_spent: i32,
    boss_hp: i32
}

impl Game {
    fn new() -> Game {
        Game {
            p_effects: Vec::new(),
            p_hp: 50, p_mana: 500, p_spent: 0,
            boss_hp: BOSS_HP
        }
    }

    fn cast(&mut self, spell: Spell) {
        let cost = spell.cost();
        if cost > self.p_mana {
            return;
        }
        self.p_spent += cost;
        self.p_mana -= cost;

        match spell {
            Spell::Missile => self.boss_hp -= 4,
            Spell::Drain => {
                self.boss_hp -= 2;
                self.p_hp += 2;
            }
            Spell::Shield => self.p_effects.push((Effect::Shield, 6)),
            Spell::Recharge => self.p_effects.push((Effect::Recharge, 5)),
            Spell::Poison => self.p_effects.push((Effect::Poison, 6)),
        }
    }

    fn apply_effects(&mut self) {
        for (e, time) in self.p_effects.iter_mut() {
            match e {
                Effect::Shield => {}
                Effect::Poison => self.boss_hp -= 3,
                Effect::Recharge => self.p_mana += 101
            }
            *time -= 1;
        }
        self.p_effects = self.p_effects.iter().filter(|e| e.1 > 0).copied().collect();
    }

    fn boss_atk(&mut self) {
        let mut dmg = BOSS_ATK;
        for (e, _) in &self.p_effects {
            if *e == Effect::Shield {
                dmg -= 7;
                break;
            }
        }
        self.p_hp -= dmg.max(1);
    }

    fn check_status(&self) -> Status {
        if self.p_hp <= 0 {
            return Status::Loss;
        } else if self.boss_hp <= 0 {
            return Status::Win;
        }
        Status::Undecided
    }
}

fn least_mana(hardcore: bool) -> i32 {
    let mut least = i32::MAX;
    let mut games: Vec<Game> = vec![Game::new()];
    while !games.is_empty() {
        let mut nxt = Vec::new();
        for mut g in games {
            g.apply_effects();
            match g.check_status() {
                Status::Win => least = least.min(g.p_spent),
                Status::Loss => continue,
                Status::Undecided => {
                    g.p_hp -= if hardcore { 1 } else { 0 };
                    for s in Spell::iter() {
                        let has_effect = g.p_effects.iter().any(
                            |e| Some(e.0) == s.effect()
                        );
                        // check if casting this spell makes sense
                        if has_effect || g.p_mana < s.cost() {
                            continue;
                        }

                        let mut new_g = g.clone();
                        new_g.cast(s);
                        match new_g.check_status() {
                            Status::Win => least = least.min(new_g.p_spent),
                            Status::Loss => continue,
                            Status::Undecided => {
                                if new_g.p_spent > least {
                                    continue;
                                }
                            }
                        }

                        new_g.apply_effects();
                        if new_g.check_status() == Status::Win
                            && new_g.p_spent < least {
                            least = new_g.p_spent;
                            continue;
                        }

                        new_g.boss_atk();
                        match new_g.check_status() {
                            Status::Win => {}  // no way this can trigger
                            Status::Loss => continue,
                            Status::Undecided => nxt.push(new_g)
                        }
                    }
                }
            }
        }
        games = nxt;
    }
    least
}

fn main() {
    println!("least mana to win (ez): {}", least_mana(false));
    println!("least mana to win (hard): {}", least_mana(true));
}
