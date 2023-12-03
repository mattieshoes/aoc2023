import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;


public class ProblemThree {
    public int[][] engine;

    // returns location of the gear near the search square
    public int[] checkGear(int r, int c) {
        for(int ro = r-1; ro <= r+1; ro++) 
            for(int co = c-1; co <= c+1; co++) 
                if(engine[ro][co] == -3) 
                    return new int[]{ro,co};
        return new int[]{-1,-1};
    }

    // returns true if a symbol is near the search square
    public boolean check(int r, int c) {
        for(int ro = r-1; ro <= r+1; ro++) 
            for(int co = c-1; co <= c+1; co++) 
                if(engine[ro][co] <= -2) 
                    return true;
        return false;
    }

    // parse numbers across squares, sum those next to a symbol.
    public void part1() {
        int tempSum = 0, sum = 0;
        boolean found = false;

        for(int r = 0; r < engine.length; r++) {
            for(int c = 0; c < engine[0].length; c++) {
                int val = engine[r][c];
                switch(val) {
                    case -1, -2, -3:
                            if(tempSum > 0 && found)
                                sum += tempSum;
                            tempSum = 0;
                            found = false;
                        break;
                    default:
                        tempSum = tempSum * 10 + val;
                        if(!found)
                            found = check(r, c);
                }
            }
        }
        System.out.println("Part 1: " + sum);
    }

    // parse numbers across squares, some products of pairs next to a gear
    public void part2() {
        class Ratio {
            public Ratio(int v, int x, int y) {
                val = v;
                gearx = x;
                geary = y;
            }
            public int val;
            public int gearx;
            public int geary;
        }
        List<Ratio> matches = new ArrayList<Ratio>();
        int[] found = {-1,-1};
        int tempSum = 0;
        int sum = 0;

        // produce list of numbers with the location of the neighboring gear
        for(int r = 0; r < engine.length; r++) {
            for(int c = 0; c < engine[0].length; c++) {
                int val = engine[r][c];
                switch(val) {
                    case -1, -2, -3: // boundary
                            if(tempSum > 0 && found[0] > -1) 
                                matches.add(new Ratio(tempSum, found[0], found[1]));
                            tempSum = 0;
                            found[0] = found[1] = -1;
                        break;
                    default: // number
                        tempSum = tempSum * 10 + val;
                        if(found[0] < 0) 
                            found = checkGear(r, c);
                }
            }
        }

        // find two values bordering the same gear, and sum the products
        for(int i = 0; i < matches.size(); i++) 
            for(int j = i + 1; j < matches.size(); j++) 
                if(matches.get(i).gearx == matches.get(j).gearx)
                    if(matches.get(i).geary == matches.get(j).geary) 
                        sum += matches.get(i).val * matches.get(j).val;
        System.out.format("Part 2: %d\n", sum);
    }

    public void solve() {
        try {
            List<String> allLines = Files.readAllLines(Paths.get("inputs/3"));

            // builds engine in a 2d int array
            // numbers are converted to their integer value
            // '.' is -1
            // '*' is -3
            // all other symbols are -2
            // surrounded with a -1 border for ease of bounds checking
            int width = allLines.get(0).length();
            int height = allLines.size();
            engine = new int[width+2][height+2];
            for(int[] row : engine) {
                Arrays.fill(row, -1);
            }
            for(int r = 0; r < height; r++) {
                for(int c = 0; c < width; c++) {
                    char val = allLines.get(r).charAt(c);

                    switch(val) {
                        case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
                            engine[r+1][c+1] = val - '0';
                            break;
                        case '.':
                            break;
                        case '*':
                            engine[r+1][c+1] = -3;
                            break;
                        default: 
                            engine[r+1][c+1] = -2;
                        
                    }
                }
            }
            part1();
            part2();

        } catch(IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String args[]) {
        ProblemThree x = new ProblemThree();
        x.solve();
    }
}
