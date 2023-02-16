use std::collections::HashMap;

const INPUT: i64 = 7989;
// const INPUT: i64 = 39;

#[derive(Debug, Eq, Hash, PartialEq)]
struct Point(i64, i64);

impl Point {
    fn rack_id(&self) -> i64 {
        self.0 + 10
    }

    fn power_level(&self) -> i64 {
        let rack_id = self.rack_id();
        let mut power_level = rack_id * self.1;
        power_level += INPUT;
        power_level *= rack_id;
        power_level = (power_level / 100) % 10;
        power_level - 5
    }
}

fn square(power_levels: &HashMap<Point, i64>, p: &Point) -> i64 {
    let mut power_level = 0;
    for x in 0i64..=2 {
        for y in 0i64..=2 {
            power_level += power_levels.get(&Point(p.0 + x, p.1 + y)).unwrap_or(&0);
        }
    }
    power_level
}

fn main() {
    let p = Point(217,196);
    println!("{p:?}, power_level: {}", p.power_level());

    let mut power_levels: HashMap<_, _> = HashMap::new();
    for x in 1i64..=300 {
        for y in 1i64..=300 {
            let p = Point(x, y);
            let power_level = p.power_level();
            power_levels.insert(p, power_level);
        }
    }

    let mut square_power_level = 0;
    for x in 1i64..=298 {
        for y in 1i64..=298 {
            let p = Point(x, y);
            let this = square(&power_levels, &p);
            if this > square_power_level {
                square_power_level = this;
                println!("Larger, {:?}, {}", p, square_power_level);
            }
        }
    }
}
