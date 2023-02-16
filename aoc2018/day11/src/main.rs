use std::collections::HashMap;

const INPUT: i32 = 7989;
// const INPUT: i32 = 39;

type Point = (i32, i32);

#[derive(Debug)]
struct Largest {
    power_level: i32,
    point: Point,
    size: i32,
}

fn rack_id(p: &Point) -> i32 {
    p.0 + 10
}

fn power_level(p: &Point) -> i32 {
    let rack_id = rack_id(p);
    let mut power_level = rack_id * p.1;
    power_level += INPUT;
    power_level *= rack_id;
    power_level = (power_level / 100) % 10;
    power_level - 5
}

fn square(power_levels: &HashMap<Point, i32>, p: &Point, size: i32) -> i32 {
    let mut power_level = 0;
    for x in 0i32..size {
        for y in 0i32..size {
            power_level += power_levels.get(&(p.0 + x, p.1 + y)).unwrap_or(&0);
        }
    }
    power_level
}

fn largest_power_level(power_levels: &HashMap<Point, i32>, size: i32) -> Largest {
    let mut largest = Largest { power_level: 0, point: (0, 0), size };

    for x in 1i32..=(300 + 1 - size) {
        for y in 1i32..=(300 + 1 - size) {
            let p = (x, y);
            let this = square(&power_levels, &p, size);
            if this > largest.power_level {
                largest.power_level = this;
                largest.point = p;
            }
        }
    }

    largest
}

fn main() {
    let mut power_levels: HashMap<_, _> = HashMap::new();
    for x in 1i32..=300 {
        for y in 1i32..=300 {
            let p = (x, y);
            power_levels.insert(p, power_level(&p));
        }
    }

    println!("Part 1: {:?}", largest_power_level(&power_levels, 3));

    let mut largest = Largest { power_level: 0, point: (0, 0), size: 0 };
    for size in 1..=300 {
        println!("Checking with size {size}");
        let this = largest_power_level(&power_levels, size);
        if this.power_level > largest.power_level {
            largest = this;
        }
    }

    println!("Part 2: {:?}", largest);
}
