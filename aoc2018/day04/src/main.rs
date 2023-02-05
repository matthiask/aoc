use std::fs;
use std::io::{self, BufRead};
use regex::Regex;

struct Guard {
    id: usize,
    asleep: Vec<usize>,
    asleep_sum: usize,
}


fn main() -> io::Result<()> {
    // let file = fs::File::open("04-test.txt")?;
    let file = fs::File::open("04.txt")?;
    let reader = io::BufReader::new(file);
    let result: Result<Vec<_>, _> = reader.lines().collect();
    let mut lines = result.unwrap();
    lines.sort();

    println!("{}", lines.len());

    let timestamp_re = Regex::new(r"\d{4}-\d{2}-\d{2} \d{2}:(\d{2})").unwrap();
    let guard_re = Regex::new(r"Guard #(\d+)").unwrap();

    let mut guards: Vec<Guard> = Vec::new();
    let mut line = 0;

    while line < lines.len() {
        let caps = guard_re.captures(&lines[line]).unwrap();
        let id = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
        let mut guard = Guard {
            id,
            asleep: vec![0; 60],
            asleep_sum: 0,
        };
        println!("Guard {}", guard.id);
        line += 1;

        loop {
            if line >= lines.len() || lines[line].contains("Guard") {
                guards.push(guard);
                break;
            }

            let start_caps = timestamp_re.captures(&lines[line]).unwrap();
            let end_caps = timestamp_re.captures(&lines[line + 1]).unwrap();
            let start = start_caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
            let end = end_caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
            line += 2;

            for i in start..(end + 1) {
                guard.asleep[i] = 1;
            }

            guard.asleep_sum += end - start;
        }
    }

    Ok(())
}
