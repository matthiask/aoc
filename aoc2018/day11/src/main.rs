use std::collections::HashMap;

const INPUT: i64 = 7989;
// const INPUT: i64 = 39;

type Point = (i64, i64);

#[derive(Debug)]
struct Largest {
    power_level: i64,
    point: Point,
    size: i64,
}

fn rack_id(p: &Point) -> i64 {
    p.0 + 10
}

fn power_level(p: &Point) -> i64 {
    let rack_id = rack_id(p);
    let mut power_level = rack_id * p.1;
    power_level += INPUT;
    power_level *= rack_id;
    power_level = (power_level / 100) % 10;
    power_level - 5
}

fn square(power_levels: &HashMap<Point, i64>, p: &Point, size: i64) -> i64 {
    let mut power_level = 0;
    for x in 0i64..size {
        for y in 0i64..size {
            power_level += power_levels.get(&(p.0 + x, p.1 + y)).unwrap_or(&0);
        }
    }
    power_level
}

fn largest_power_level(power_levels: &HashMap<Point, i64>, size: i64) -> Largest {
    let mut largest = Largest { power_level: 0, point: (0, 0), size };

    for x in 1i64..=(300 + 1 - size) {
        for y in 1i64..=(300 + 1 - size) {
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
    for x in 1i64..=300 {
        for y in 1i64..=300 {
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
