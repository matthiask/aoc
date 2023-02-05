use std::fs;

fn react(s: &String) -> String {
    let mut chars: Vec<char> = s.chars().collect();

    'outer: loop {
        for i in 0..(chars.len() - 1) {
            let c1 = chars[i];
            let c2 = chars[i + 1];

            if (c1 < 'a' && c2 >= 'a' && (c2 as u32 - c1 as u32) == 32)
                || (c1 >= 'a' && c2 < 'a' && (c1 as u32 - c2 as u32) == 32)
            {
                chars.remove(i);
                chars.remove(i);
                continue 'outer;
            }
        }
        break;
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
}
