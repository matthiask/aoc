use std::collections::HashSet;
use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Before {
    required: char,
    step: char,
    seconds: u32,
}

fn parse_before(s: &str) -> Before {
    let tokens: Vec<&str> = s.split_whitespace().collect();
    let required = tokens[1].chars().next().unwrap();
    let step = tokens[7].chars().next().unwrap();
    let seconds = (step as u32) - 64 + 60;
    Before {
        required,
        step,
        seconds,
    }
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let pairs: Vec<Before> = reader
        .lines()
        .map(|line| parse_before(&line.unwrap()))
        .collect();

    println!("pairs: {}", pairs.len());
    println!("{:?}", &pairs);

    let mut todo: HashSet<char> = HashSet::new();
    let mut seen: HashSet<char> = HashSet::new();
    for pair in &pairs {
        todo.insert(pair.required);
        todo.insert(pair.step);
    }
    println!("{:?}", &todo);

    let mut result: Vec<char> = vec![];

    while todo.len() > 0 {
        let mut next: Vec<char> = todo
            .iter()
            .filter(|c| {
                pairs
                    .iter()
                    .filter(|p| p.step == **c)
                    .all(|p| seen.contains(&p.required))
            })
            .copied()
            .collect();
        next.sort();
        println!("{:?}", next);
        for c in next {
            todo.remove(&c);
            seen.insert(c);

            result.push(c);

            // Only always take the first and begin again; toposort would have been nice as well...
            break;
        }
    }

    println!("Part 1: {}", result.into_iter().collect::<String>());
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
