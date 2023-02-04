use std::fs;
use std::io::{self, BufRead};
use std::collections::HashMap;
// use std::iter::zip;

#[derive(Copy, Clone)]
struct Rect {
    id: i64,
    x: i64,
    y: i64,
    w: i64,
    h: i64,
}

impl Rect {
    fn x_outside(&self) -> i64 {
        self.x + self.w
    }

    fn y_outside(&self) -> i64 {
        self.y + self.h
    }

    fn overlaps(&self, other: &Rect) -> bool {
        self.x_outside() >= other.x
            && other.x_outside() >= self.x
            && self.y_outside() >= other.y
            && other.y_outside() >= self.y
    }
}

fn parse_claim(line: &str) -> Rect {
    let parts: Vec<&str> = line
        .split(&[' ', '#', ',', ':', 'x', '#', '@'][..])
        .collect();
    // println!("parts: {:?}", &parts);
    Rect {
        id: parts[1].parse::<i64>().unwrap(),
        x: parts[4].parse::<i64>().unwrap(),
        y: parts[5].parse::<i64>().unwrap(),
        w: parts[7].parse::<i64>().unwrap(),
        h: parts[8].parse::<i64>().unwrap(),
    }
}

fn main() -> io::Result<()> {
    // let file = fs::File::open("03-test.txt")?;
    let file = fs::File::open("03.txt")?;
    let reader = io::BufReader::new(file);

    let mut claims = Vec::new();

    for line in reader.lines() {
        claims.push(parse_claim(&line.unwrap()));
    }

    println!("claims: {}", claims.len());

    let mut occupations: HashMap<i64, i64> = HashMap::new();
    for claim in &claims {
        for x in claim.x..claim.x_outside() {
            for y in claim.y..claim.y_outside() {
                let v = y * 10000 + x;
                let n = occupations.get(&v).unwrap_or(&0);
                occupations.insert(v, n + 1);
            }
        }
    }
    let mut more_than_one = 0;
    for value in occupations.values() {
        if value > &1 {
            more_than_one += 1;
        }
    }

    println!("part1: {}", more_than_one);

    'outer: for i in 0..claims.len() {
        for j in 0..claims.len() {
            if i != j && claims[i].overlaps(&claims[j]) {
                continue 'outer;
            }
        }

        println!("part2: {}", &claims[i].id);
        break;
    }

    Ok(())
}
