use std::fs;
use std::io::{self, BufRead};
use std::collections::HashMap;
// use std::iter::zip;

#[derive(Copy, Clone)]
struct Rect {
    x: i64,
    y: i64,
    w: i64,
    h: i64,
    negative: bool,
}

impl Rect {
    fn x_outside(&self) -> i64 {
        self.x + self.w
    }

    fn y_outside(&self) -> i64 {
        self.y + self.h
    }

    fn size(&self) -> i64 {
        let area = self.w * self.h ;
        if self.negative {
            return -area;
        }
        area
    }

    fn intersect(&self, other: &Rect) -> Option<Rect> {
        if !self.overlaps(&other) {
            return None;
        }
        let x = std::cmp::max(self.x, other.x);
        let y = std::cmp::max(self.y, other.y);
        let w = std::cmp::min(self.x_outside(), other.x_outside()) - x;
        let h = std::cmp::min(self.y_outside(), other.y_outside()) - y;
        Some(Rect {
            x,
            y,
            w,
            h,
            negative: true,
        })
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
        x: parts[4].parse::<i64>().unwrap(),
        y: parts[5].parse::<i64>().unwrap(),
        w: parts[7].parse::<i64>().unwrap(),
        h: parts[8].parse::<i64>().unwrap(),
        negative: false,
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

    /*
    let mut rects = Vec::new();
    for rect in claims {
        for i in 0..rects.len() {
            if let Some(x) = rect.intersect(&rects[i]) {
                rects.push(rect);
                rects.push(rects[i]);
                rects.push(x);
            }
        }
        rects.push(rect);
    }

    let mut area = 0;
    for rect in rects {
        area += rect.size();
    }

    println!("area: {}", area);
    */

    let mut occupations: HashMap<i64, i64> = HashMap::new();
    for claim in claims {
        for dx in 0..claim.w {
            for dy in 0..claim.h {
                let v = (claim.y + dy) * 10000 + (claim.x + dx);
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

    Ok(())
}
