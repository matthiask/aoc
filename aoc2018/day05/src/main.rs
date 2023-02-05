use std::cmp;
use std::fs;

fn react(s: &String) -> String {
    let mut chars: Vec<char> = s.chars().collect();
    let mut i = 0;

    while i < chars.len() - 1 {
        let c1 = chars[i];
        let c2 = chars[i + 1];

        if (c1 < 'a' && c2 >= 'a' && (c2 as u32 - c1 as u32) == 32)
            || (c1 >= 'a' && c2 < 'a' && (c1 as u32 - c2 as u32) == 32)
        {
            chars.remove(i);
            chars.remove(i);
            if i > 0 {
                i -= 1;
            }
        } else {
            i += 1;
        }
    }

    chars.into_iter().collect()
}

fn main() {
    let test = String::from("dabAcCaCBAcCcaDA");
    println!(
        "{} -> {} (length {})",
        test,
        react(&test),
        react(&test).len()
    );

    let content = String::from(fs::read_to_string("05.txt").unwrap().trim());
    println!("Part 1: {}", react(&content).len());

    let mut min_length = 999999;
    for c in 'a'..'{' {
        let len = react(&String::from(
            content
                .replace(c, "")
                .replace(char::from_u32((c as u32) - 32).unwrap(), ""),
        ))
        .len();
        println!("Part 2: without char {}: {}", c, len);
        min_length = cmp::min(min_length, len);
    }
    println!("Part 2: {}", min_length);
}
