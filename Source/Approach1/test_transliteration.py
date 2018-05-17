import CandidateSet
import TransliterationModel.Transliteration as Transliteration
import utilities

def main():
    EtoV_dev_list = utilities.read_align_file('../../../Alignment_Split/EtoV_Test.txt')
    VtoE_dev_list = utilities.read_align_file('../../../Alignment_Split/VtoE_Test.txt')
    # CandidateSet.createCandidateSet(EtoV_dev_list,VtoE_dev_list,'test')
    pair = ([10, 11], [12, 13, 14, 15], 'PERSON', 'Richard Matsch', 'Thẩm phán Richard Matsch', 'PERSON', 2, 1)
    print('Candidate',CandidateSet.getCandidateSetFromFile(2)[7],'test')
    tmp = Transliteration.getTransliterationProb(pair,'')
    print(tmp)


if __name__ == '__main__':
    main()