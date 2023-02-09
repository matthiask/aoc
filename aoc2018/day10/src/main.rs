use regex::Regex;
use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Point {
    initial: (i32, i32),
    velocity: (i32, i32),
}

type Points = Vec<Point>;
type Positions = Vec<(i32, i32)>;

impl Point {
    fn position(&self, time: i32) -> (i32, i32) {
        (
            self.initial.0 + time * self.velocity.0,
            self.initial.1 + time * self.velocity.1,
        )
    }
}

fn parse_point(line: &str) -> Point {
    let numbers_re = Regex::new(r"([-\d]+)").unwrap();
    let numbers: Vec<i32> = numbers_re
        .captures_iter(&line)
        .map(|c| c.get(1).unwrap().as_str().parse::<i32>().unwrap())
        .collect();

    Point {
        initial: (numbers[0], numbers[1]),
        velocity: (numbers[2], numbers[3]),
    }
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let points: Points = reader.lines().map(|c| parse_point(&c.unwrap())).collect();

    println!("{points:?}");

    let mut time = 0;
    loop {
        let positions: Positions = points.iter().map(|point| point.position(time)).collect();

        let y_max = positions.iter().map(|p| p.1).max().unwrap();
        let y_min = positions.iter().map(|p| p.1).min().unwrap();

        if y_max - y_min <= 7 {
            break;
        }

        time += 1;

        // println!("{positions:?}");
        // println!("y diff: {}",y_max - y_min);
    }

    println!("Time {}", time);

    // println!("part 1: {}", metadata.iter().sum::<i32>());
    // println!("part 2: {}", node_value(&mut numbers.iter()));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
