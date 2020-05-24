package genefinder;

public class GeneFinder {
    private String data;
    private int currentPosition = 0;

    public GeneFinder(String filename) {
        FileResource file = new FileResource("src/genefinder/src/"+filename);
        String data = file.getData();
        this.data = data;
    }

    public String getNextGene() {
        int startPosition = this.data.indexOf("atg", this.currentPosition);
        int finishPosition;
        boolean found = false;
        while (true) {
            startPosition = this.data.indexOf("atg", startPosition + 1);
            if (startPosition == -1) {
                this.currentPosition = -1;
                return "";
            }
            int tmpPosition = startPosition;
            while(true) {
                finishPosition = this.data.indexOf("taa", tmpPosition + 1);
                if (finishPosition == -1) {
                    break;
                } else if ((finishPosition - startPosition) % 3 == 0) {
                    this.currentPosition = finishPosition;
                    return this.data.substring(startPosition, finishPosition+3);
                } else {
                    tmpPosition = finishPosition;
                }
            }
        }
    }
}

