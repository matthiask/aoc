use regex::Regex;
use std::collections::HashMap;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone)]
struct Guard {
    id: usize,
    asleep: [usize; 60],
}

fn main() -> io::Result<()> {
    // let file = fs::File::open("04-test.txt")?;
    let file = fs::File::open("04.txt")?;
    let reader = io::BufReader::new(file);
    let result: Result<Vec<_>, _> = reader.lines().collect();
    let mut lines = result.unwrap();
    lines.sort();

    // println!("Lines {}", lines.len());

    let timestamp_re = Regex::new(r"\d{4}-\d{2}-\d{2} \d{2}:(\d{2})").unwrap();
    let guard_re = Regex::new(r"Guard #(\d+)").unwrap();

    let mut guards: Vec<Guard> = Vec::new();
    let mut line = 0;

    while line < lines.len() {
        let caps = guard_re.captures(&lines[line]).unwrap();
        let id = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
        let mut guard = Guard {
            id,
            asleep: [0; 60],
        };
        // println!("Guard {}", guard.id);
        line += 1;

        loop {
            if line >= lines.len() || lines[line].contains("Guard") {
                guards.push(guard);
                break;
            }

            let start_caps = timestamp_re.captures(&lines[line]).unwrap();
            let end_caps = timestamp_re.captures(&lines[line + 1]).unwrap();
            let start = start_caps
                .get(1)
                .unwrap()
                .as_str()
                .parse::<usize>()
                .unwrap();
            let end = end_caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
            line += 2;

            for i in start..end {
                guard.asleep[i] = 1;
            }
        }
    }

    let mut most_asleep: HashMap<usize, usize> = HashMap::new();
    for guard in &guards {
        most_asleep.insert(
            guard.id,
            most_asleep.get(&guard.id).unwrap_or(&0) + guard.asleep.iter().sum::<usize>(),
        );
    }

    let mut sleepiest_guard_id: usize = 0;
    let mut sleepiest_guard_minutes: usize = 0;
    for (key, val) in most_asleep.iter() {
        if *val > sleepiest_guard_minutes {
            sleepiest_guard_minutes = *val;
            sleepiest_guard_id = *key;
        }
    }

    println!(
        "Sleepiest guard: {} ({} minutes)",
        sleepiest_guard_id, sleepiest_guard_minutes
    );

    let sleepiest_guard_nights: Vec<Guard> = guards
        .into_iter()
        .filter(|g| g.id == sleepiest_guard_id)
        .collect();
    let mut sleepiest_minute: usize = 0;
    let mut sleepiest_minute_minutes: usize = 0;

    for minute in 0..60 {
        let total: usize = sleepiest_guard_nights
            .iter()
            .map(|g| g.asleep[minute])
            .sum();
        // println!("debug: {} {}", minute, total);
        if total > sleepiest_minute_minutes {
            sleepiest_minute = minute;
            sleepiest_minute_minutes = total;
        }
    }

    println!("Sleepiest minute: {}", sleepiest_minute);
    println!("Part 1: {}", sleepiest_guard_id * sleepiest_minute);

    Ok(())
}
