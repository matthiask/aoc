use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone)]
struct Coords {
    x: i32,
    y: i32,
}

fn coords_from_str(s: &str) -> Coords {
    let pair = s.split_once(", ").unwrap();
    let x = pair.0.parse::<i32>().unwrap();
    let y = pair.1.parse::<i32>().unwrap();
    Coords { x, y }
}

fn main() {
    let file = fs::File::open("06-test.txt").unwrap();
    // let file = fs::File::open("06.txt").unwrap();
    let reader = io::BufReader::new(file);

    let coords: Vec<Coords> = reader
        .lines()
        .map(|line| coords_from_str(&line.unwrap()))
        .collect();

    println!("coords: {}", coords.len());
}
