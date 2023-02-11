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

struct BoundingBox(i32, i32, i32, i32);

impl BoundingBox {
    fn from_positions(positions: &Positions) -> Self {
        let x: Vec<i32> = positions.iter().map(|p| p.0).collect();
        let y: Vec<i32> = positions.iter().map(|p| p.1).collect();

        BoundingBox(
            *x.iter().min().unwrap(),
            *y.iter().min().unwrap(),
            *x.iter().max().unwrap(),
            *y.iter().max().unwrap(),
        )
    }
}

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

fn print(positions: &Positions) {
    let bbox = BoundingBox::from_positions(positions);

    let width = (bbox.2 - bbox.0 + 1) as usize;
    let height = (bbox.3 - bbox.1 + 1) as usize;

    if width < 100 && height < 100 {
        let mut grid: Vec<Vec<char>> = Vec::new();
        for _y in 0..height {
            let mut row: Vec<char> = vec![' '; width];
            // row.fill(' ');
            grid.push(row);
        }
        for p in positions {
            grid[(p.1 - bbox.1) as usize][(p.0 - bbox.0) as usize] = 'x';
        }

        println!("");
        for row in grid {
            println!("{}", row.into_iter().collect::<String>());
        }
        println!("");
    } else {
        println!("Too large");
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

        println!("Time {}", time);
        print(&positions);

        time += 1;

        // println!("{positions:?}");
        // println!("y diff: {}",y_max - y_min);
    }

    // println!("part 1: {}", metadata.iter().sum::<i32>());
    // println!("part 2: {}", node_value(&mut numbers.iter()));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
