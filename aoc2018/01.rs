use std::fs;
use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    // Open the file in read-only mode with buffer.
    let file = fs::File::open("01.txt")?;
    let reader = io::BufReader::new(file);

    // Read the file line by line.
    let mut numbers = Vec::new();
    for line in reader.lines() {
        // Parse each line as a number.
        match line?.parse::<i32>() {
            Ok(n) => numbers.push(n),
            Err(e) => {
                println!("Error: {}", e)
            }
        }
    }

    // Do something with the numbers.
    let mut freq = 0;
    for number in numbers {
        freq += number;
    }
    println!("freq: {}", freq);

    Ok(())
}
