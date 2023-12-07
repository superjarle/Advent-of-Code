use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::error::Error;

fn make_maps(data: &[String]) -> Vec<(i32, i32, i32)> {
    let mut maps: Vec<_> = data.iter().filter_map(|line| {
        let parts: Vec<i32> = line.split_whitespace()
                                  .filter_map(|s| s.parse().ok())
                                  .collect();
        if parts.len() == 3 {
            Some((parts[1], parts[1] + parts[2], parts[0]))
        } else {
            None
        }
    }).collect();

    maps.sort_unstable();
    maps
}

fn convert(value: i32, maps: &[(i32, i32, i32)]) -> i32 {
    maps.iter()
        .find(|&&(src_start, src_end, _)| src_start <= value && value < src_end)
        .map_or(value, |&(src_start, _, dest_start)| value - src_start + dest_start)
}

fn read_from_file(filename: &Path) -> Result<(Vec<(i32, i32)>, Vec<Vec<String>>), Box<dyn Error>> {
    let file = File::open(filename)?;
    let lines: Vec<String> = io::BufReader::new(file).lines().collect::<Result<_, _>>()?;

    let seeds = lines.get(0).ok_or("No seed line found")?
                      .split(": ").nth(1).ok_or("Incorrect seed line format")?
                      .split_whitespace()
                      .collect::<Vec<_>>()
                      .chunks(2)
                      .filter_map(|chunk| Some((chunk.get(0)?.parse().ok()?, chunk.get(1)?.parse().ok()?)))
                      .collect();

    let mut stages = Vec::new();
    let mut stage = Vec::new();
    for line in lines.iter().skip(1) {
        if line.ends_with(" map:") {
            if !stage.is_empty() {
                stages.push(stage.clone());
                stage.clear();
            }
        } else if !line.is_empty() {
            stage.push(line.clone());
        }
    }
    if !stage.is_empty() {
        stages.push(stage);
    }

    Ok((seeds, stages))
}

fn lowest_location(filename: &str) -> Result<i32, Box<dyn Error>> {
    let path = Path::new(filename);
    let (seeds, data) = read_from_file(&path)?;

    let maps_list: Vec<_> = data.iter().map(|stage| make_maps(stage)).collect();

    let min_location = seeds.iter()
                            .map(|&(start, _)| maps_list.iter().fold(start, |location, maps| convert(location, maps)))
                            .min()
                            .ok_or("No minimum location found")?;

    Ok(min_location)
}

fn main() {
    let filename = "day5.txt";

    match lowest_location(filename) {
        Ok(result) => println!("Lowest location: {}", result),
        Err(e) => eprintln!("Error: {}", e),
    }
}
