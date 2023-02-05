use itertools::iproduct;
use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
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

fn manhattan_distance(c1: &Coords, c2: &Coords) -> i32 {
    (c1.x - c2.x).abs() + (c1.y - c2.y).abs()
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let coords: Vec<Coords> = reader
        .lines()
        .map(|line| coords_from_str(&line.unwrap()))
        .collect();

    println!("coords: {}", coords.len());
    for i in 0..coords.len() {
        for j in i + 1..coords.len() {
            println!(
                "{:?} <-> {:?} : {}",
                &coords[i],
                &coords[j],
                manhattan_distance(&coords[i], &coords[j])
            );
        }
    }

    let max_distance = iproduct!(&coords, &coords)
        .map(|(c1, c2)| manhattan_distance(c1, c2))
        .max()
        .unwrap();
    println!("max distance: {}", max_distance);
}

fn main() {
    for filename in env::args().skip(1) {
        process(&filename);
    }
}
