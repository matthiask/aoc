use std::fs;
use std::io::{self, BufRead};
// use std::iter::zip;

struct Rect {
    x: usize,
    y: usize,
    w: usize,
    h: usize,
    negative: bool,
}

impl Rect {
    fn x_outside(&self) -> usize {
        self.x + self.w
    }

    fn y_outside(&self) -> usize {
        self.y + self.h
    }

    fn size(&self) -> usize {
        self.w * self.h
    }

    fn intersect(&self, other: &Rect) -> Option<Rect> {
        None
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
        x: parts[4].parse::<usize>().unwrap(),
        y: parts[5].parse::<usize>().unwrap(),
        w: parts[7].parse::<usize>().unwrap(),
        h: parts[8].parse::<usize>().unwrap(),
        negative: false,
    }
}

fn main() -> io::Result<()> {
    let file = fs::File::open("03.txt")?;
    let reader = io::BufReader::new(file);

    let mut claims = Vec::new();

    for line in reader.lines() {
        claims.push(parse_claim(&line.unwrap()));
    }

    println!("claims: {}", claims.len());

    let mut rects = Vec::new();
    for rect in claims {
        for inter in &rects.clone() {
            if let Some(x) = rect.intersect(&inter) {
                rects.push(x);
            }
        }
        rects.push(rect);
    }

    Ok(())
}
