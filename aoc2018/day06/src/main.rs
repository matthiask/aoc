use itertools::iproduct;
use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct BBox {
    x_min: i32,
    x_max: i32,
    y_min: i32,
    y_max: i32,
}

fn coords_from_str(s: &str) -> Point {
    let pair = s.split_once(", ").unwrap();
    let x = pair.0.parse::<i32>().unwrap();
    let y = pair.1.parse::<i32>().unwrap();
    Point { x, y }
}

fn bbox_from_coords(coords: &Vec<Point>) -> BBox {
    let x_min = coords.iter().map(|c| c.x).min().unwrap();
    let x_max = coords.iter().map(|c| c.x).max().unwrap();
    let y_min = coords.iter().map(|c| c.y).min().unwrap();
    let y_max = coords.iter().map(|c| c.y).max().unwrap();
    return BBox {
        x_min,
        x_max,
        y_min,
        y_max,
    };
}

fn manhattan_distance(c1: &Point, c2: &Point) -> i32 {
    (c1.x - c2.x).abs() + (c1.y - c2.y).abs()
}

fn nearest(coords: &Vec<Point>, point: &Point) -> Option<usize> {
    let mut intermediate: Vec<(usize, i32)> = coords
        .iter()
        .enumerate()
        .map(|(idx, c)| (idx, manhattan_distance(c, point)))
        .collect();
    intermediate.sort_unstable_by(|a, b| a.1.cmp(&b.1));
    // println!("Point: {:?}, intermediate: {:?}", point, intermediate);
    if intermediate[0].1 != intermediate[1].1 {
        return Some(intermediate[0].0);
    }
    None
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let coords: Vec<Point> = reader
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
    println!("Bounding box: {:?}", bbox_from_coords(&coords));

    let mut sizes: Vec<i64> = vec![0; coords.len()];
    let bbox = bbox_from_coords(&coords);
    /* Outside borders */
    for x in bbox.x_min - 1..bbox.x_max + 1 {
        if let Some(id) = nearest(
            &coords,
            &Point {
                x,
                y: bbox.y_min - 1,
            },
        ) {
            sizes[id] = i32::MAX as i64;
        }
        if let Some(id) = nearest(
            &coords,
            &Point {
                x,
                y: bbox.y_max + 1,
            },
        ) {
            sizes[id] = i32::MAX as i64;
        }
    }
    for y in bbox.y_min - 1..bbox.y_max + 1 {
        if let Some(id) = nearest(
            &coords,
            &Point {
                x: bbox.x_min - 1,
                y,
            },
        ) {
            sizes[id] = i32::MAX as i64;
        }
        if let Some(id) = nearest(
            &coords,
            &Point {
                x: bbox.x_max + 1,
                y,
            },
        ) {
            sizes[id] = i32::MAX as i64;
        }
    }
    /* Inside */
    for x in bbox.x_min..bbox.x_max {
        for y in bbox.y_min..bbox.y_max {
            if let Some(id) = nearest(&coords, &Point { x, y }) {
                sizes[id] += 1;
            }
        }
    }
    println!(
        "Part 1: {}",
        sizes
            .iter()
            .filter(|size| *size < &(i32::MAX as i64))
            .max()
            .unwrap()
    );
}

fn main() {
    for filename in env::args().skip(1) {
        process(&filename);
    }
}
