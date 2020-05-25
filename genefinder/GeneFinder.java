package genefinder;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class GeneFinder {
    private String dna;
    private int currentPosition = 0;

    public GeneFinder(String filename) {
        FileResource file = new FileResource("src/genefinder/src/"+filename);
        this.dna = file.getData();
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

}

