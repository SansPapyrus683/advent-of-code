use strum_macros::EnumIter;

#[derive(Debug, EnumIter, Eq, PartialEq, Hash, Copy, Clone)]
pub enum Op {
    Addr,
    Addi,
    Mulr,
    Muli,
    Banr,
    Bani,
    Borr,
    Bori,
    Setr,
    Seti,
    Gtir,
    Gtri,
    Gtrr,
    Eqir,
    Eqri,
    Eqrr,
}

impl Op {
    pub fn apply(&self, mut reg: Vec<i32>, a: i32, b: i32, c: i32) -> Vec<i32> {
        reg[c as usize] = match self {
            Op::Addr => reg[a as usize] + reg[b as usize],
            Op::Addi => reg[a as usize] + b,
            Op::Mulr => reg[a as usize] * reg[b as usize],
            Op::Muli => reg[a as usize] * b,
            Op::Banr => reg[a as usize] & reg[b as usize],
            Op::Bani => reg[a as usize] & b,
            Op::Borr => reg[a as usize] | reg[b as usize],
            Op::Bori => reg[a as usize] | b,
            Op::Setr => reg[a as usize],
            Op::Seti => a,
            Op::Gtir => i32::from(a > reg[b as usize]),
            Op::Gtri => i32::from(reg[a as usize] > b),
            Op::Gtrr => i32::from(reg[a as usize] > reg[b as usize]),
            Op::Eqir => i32::from(a == reg[b as usize]),
            Op::Eqri => i32::from(reg[a as usize] == b),
            Op::Eqrr => i32::from(reg[a as usize] == reg[b as usize]),
        };
        reg
    }

    pub fn from_str(string: &str) -> Option<Self> {
        match string {
            "addr" => Some(Self::Addr),
            "addi" => Some(Self::Addi),
            "mulr" => Some(Self::Mulr),
            "muli" => Some(Self::Muli),
            "banr" => Some(Self::Banr),
            "bani" => Some(Self::Bani),
            "borr" => Some(Self::Borr),
            "bori" => Some(Self::Bori),
            "setr" => Some(Self::Setr),
            "seti" => Some(Self::Seti),
            "gtir" => Some(Self::Gtir),
            "gtri" => Some(Self::Gtri),
            "gtrr" => Some(Self::Gtrr),
            "eqir" => Some(Self::Eqir),
            "eqri" => Some(Self::Eqri),
            "eqrr" => Some(Self::Eqrr),
            _ => None
        }
    }
}
