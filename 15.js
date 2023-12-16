#!/usr/bin/node

fs = require("fs");
let data = fs.readFileSync("inputs/15").toString().trim().split(",");

function hash(val) {
    hv = 0;
    for(let i = 0; i < val.length; i++) {
        hv += val.charCodeAt(i);
        hv *= 17;
        hv %= 256;
    }
    return hv;
}

let part1 = 0;
for(let i = 0; i < data.length; i++) {
    part1 += hash(data[i]);
}
console.log(`Part 1: ${sum}`);

function Lens(label, power) {
    this.label = label;
    this.power = power;
}

let boxes = [];
for(let i = 0; i < 256; i++) {
    boxes.push([]);
}

for(let i = 0; i < data.length; i++) {
    if(data[i].includes("=")) { // add lens to slot or modify slot with matching label
        let [label, power] = data[i].split('=');
        let boxNum = hash(label);
        let found = false
        for(let slot = 0; slot < boxes[boxNum].length; slot++) {
            if(boxes[boxNum][slot].label == label) { // modify existing
                found = true;
                boxes[boxNum][slot].power = power;
                break;
            }
        }
        if(!found) { // otherwise, add box
            boxes[boxNum].push(new Lens(label, power));
        }
    } else { // remove from box
        let label = data[i].slice(0,-1)
        let boxNum = hash(label)
        for(let slot = 0; slot < boxes[boxNum].length; slot++) {
            if(boxes[boxNum][slot].label == label) {
                boxes[boxNum].splice(slot, 1);
                break;
            }
        }
    }
}

let part2 = 0
for(let box = 0; box < boxes.length; box++) {
    for(let slot = 0; slot < boxes[box].length; slot++) {
        part2 += (box+1) * (slot+1) * boxes[box][slot].power;
    }
}
console.log(`Part 2: ${part2}`);
