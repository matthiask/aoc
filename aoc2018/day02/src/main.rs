use levenshtein::levenshtein;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;
use std::io::{self, BufRead};
use std::iter::zip;

type Frequencies = HashMap<i32, i32>;

fn count_frequencies(id: &str, frequencies: &mut Frequencies) {
    let mut count_bytes: HashMap<u8, i32> = HashMap::new();

    for byte in id.bytes() {
        let current = count_bytes.get(&byte).unwrap_or(&0);
        count_bytes.insert(byte, current + 1);
    }

    // println!("{}", count_bytes);
    let mut seen_frequency: HashSet<i32> = HashSet::new();

    for (_byte, freq) in &count_bytes {
        if freq > &1 && !seen_frequency.contains(freq) {
            let current = frequencies.get(&freq).unwrap_or(&0);
            frequencies.insert(*freq, current + 1);
            seen_frequency.insert(*freq);
        }
    }
}

fn find_closest_strings(lines: &Vec<String>) -> (usize, usize) {
    for i in 0..lines.len() {
        for j in i..lines.len() {
            let a = &lines[i];
            let b = &lines[j];
            let distance = levenshtein(&a, &b);
            if distance == 1 {
                return (i, j);
                // println!("{} .. {}: {}", a, b, distance);
            }
        }
    }
    (0, 0)
}

fn remove_mismatch(a: &str, b: &str) -> String {
    let zipper = zip(a.chars(), b.chars());
    let mut chars: Vec<char> = Vec::new();

    for (c1, c2) in zipper {
        if c1 == c2 {
            chars.push(c1);
        }
    }

    chars.iter().collect()
    // "Nothing".to_string()
}

fn main() -> io::Result<()> {
    let file = fs::File::open("02.txt")?;
    let reader = io::BufReader::new(file);

    let mut frequencies: Frequencies = HashMap::new();
    let mut lines: Vec<String> = Vec::new();

    for line in reader.lines() {
        let v = line.unwrap();
        count_frequencies(&v, &mut frequencies);
        lines.push(v);
    }

    let times_2 = frequencies.get(&2).unwrap_or(&0);
    let times_3 = frequencies.get(&3).unwrap_or(&0);

    println!("2: {}, 3: {}", &times_2, &times_3);
    println!("checksum: {}", times_2 * times_3);

    let (i, j) = find_closest_strings(&lines);
    println!("{}, {}", i, j);

    println!(
        "without mismatch: {}",
        remove_mismatch(&lines[i], &lines[j])
    );

    Ok(())
}
