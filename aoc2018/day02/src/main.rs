use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;
use std::io::{self, BufRead};

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

fn main() -> io::Result<()> {
    let file = fs::File::open("02.txt")?;
    let reader = io::BufReader::new(file);

    let mut frequencies: Frequencies = HashMap::new();

    for line in reader.lines() {
        count_frequencies(&line.unwrap(), &mut frequencies);
    }

    let times_2 = frequencies.get(&2).unwrap_or(&0);
    let times_3 = frequencies.get(&3).unwrap_or(&0);

    println!("2: {}, 3: {}", &times_2, &times_3);
    println!("checksum: {}", times_2 * times_3);

    Ok(())
}
