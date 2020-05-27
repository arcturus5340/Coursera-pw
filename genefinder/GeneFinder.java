package genefinder;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class GeneFinder {
    private String dna;
    private int currentPosition = 0;

    public GeneFinder(String filename) {
        FileResource file = new FileResource("src/genefinder/src/"+filename);
        this.dna = file.getData();
    }

    public static double cgRatio(String dnaFragment) {
        long cCount = dnaFragment.chars().filter(ch -> ch == 'c').count();
        long gCount = dnaFragment.chars().filter(ch -> ch == 'g').count();
        return (double)(cCount + gCount) / dnaFragment.length();
    }

    public static double countCTG(String dnaFragment) {
        int lastIndex = 0;
        int count = 0;

        while (lastIndex != -1) {
            lastIndex = dnaFragment.indexOf("ctg", lastIndex);
            if (lastIndex != -1) {
                if (lastIndex % 3 == 0) { count++; }
                lastIndex += 1;
            }
        }
        return count;
    }

    public List<String> getAllGenes() {
        List<String> geneStorage = new ArrayList<String>();
        String gene = this.getNextGene();
        while (!gene.equals("")) {
            geneStorage.add(gene);
            gene = this.getNextGene();
        }
        return geneStorage;
    }

    private int findStopCodon(String codon, int position) {
        int finishPosition;
        int tmpPosition = position;
        while (true) {
            finishPosition = this.dna.indexOf(codon, tmpPosition + 1);
            if (finishPosition == -1) {
                return this.dna.length();
            } else if ((finishPosition - position) % 3 == 0) {
                return finishPosition + 3;
            } else {
                tmpPosition = finishPosition;
            }
        }
    }

    public String getNextGene() {
        int startPosition = this.dna.indexOf("atg", this.currentPosition);
        while (true) {
            if (startPosition == -1) {
                this.currentPosition = 0;
                return "";
            }
            int taa_pos = findStopCodon("taa", startPosition);
            int tag_pos = findStopCodon("tag", startPosition);
            int tga_pos = findStopCodon("tga", startPosition);
            int min_pos = Math.min(Math.min(taa_pos, tag_pos), tga_pos);
            if (min_pos != this.dna.length()) {
                this.currentPosition = min_pos;
                return this.dna.substring(startPosition, min_pos);
            }
            startPosition = this.dna.indexOf("atg", startPosition + 1);
        }
    }

    public void processGenes(List<String> geneStorage) {
        List<String> longGenes = geneStorage.stream().filter(gene -> gene.length() > 9).collect(Collectors.toList());
        System.out.println("Gene that are longer than 9 characters: (" + longGenes.size() + ")");
        System.out.println(longGenes);
        List<String> highCGRatioGenes = geneStorage.stream().filter(gene -> GeneFinder.cgRatio(gene) > 0.35).collect(Collectors.toList());
        System.out.println("Gene that C-G-Ratio is higher than 9 characters: (" + highCGRatioGenes.size() + ")");
        System.out.println(highCGRatioGenes);
        String longestGene = Collections.max(geneStorage, Comparator.comparing(String::length));
        System.out.println("The longest Gene: (" + longestGene.length() + ")");
        System.out.println(longestGene);
    }
}

