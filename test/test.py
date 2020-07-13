import unittest
import scrape
import os 

class ScrapeTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        cmd="https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589 -f test -i -c -a -l -j"
        scrape.main(cmd.split(" "))

    def test_chords(self):
        foldertest="test/"
        foldertestfiles="test/testfiles/"
        name="Perfect-Ed Sheeran-chords.txt"
        with open(foldertestfiles+name,"r") as f_good, open(foldertest+name,"r") as f_test:
            self.assertEqual(f_good.read(),f_test.read())

    def test_lyrics(self):
        foldertest="test/"
        foldertestfiles="test/testfiles/"
        name="Perfect-Ed Sheeran-lyrics.txt"
        with open(foldertestfiles+name,"r") as f_good, open(foldertest+name,"r") as f_test:
            self.assertEqual(f_good.read(),f_test.read())

    def test_all(self):
        foldertest="test/"
        foldertestfiles="test/testfiles/"
        name="Perfect-Ed Sheeran-all.txt"
        with open(foldertestfiles+name,"r") as f_good, open(foldertest+name,"r") as f_test:
            self.assertEqual(f_good.read(),f_test.read())

    def test_json(self):
        foldertest="test/"
        foldertestfiles="test/testfiles/"
        name="Perfect-Ed Sheeran.json"
        with open(foldertestfiles+name,"r") as f_good, open(foldertest+name,"r") as f_test:
            self.assertEqual(f_good.read(),f_test.read())

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("test/Perfect-Ed Sheeran-chords.txt")
            os.remove("test/Perfect-Ed Sheeran-lyrics.txt")
            os.remove("test/Perfect-Ed Sheeran-all.txt")
            os.remove("test/Perfect-Ed Sheeran.json")
        except:
            print("An error has occured, files not removed.")

if __name__ == "__main__" :
    unittest.main()