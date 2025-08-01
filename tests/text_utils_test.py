import unittest
import pathlib
import pandas as pd


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup code here
        print("Setup before any tests")
        cls.test_folder = pathlib.Path.cwd() / "test_data"

    def test_get_delimited_records_from_file(self):
        from sampytools.text_utils import get_delimited_records_from_file

        testfile = self.test_folder / "delimited_text.txt"
        records = get_delimited_records_from_file(
            testfile, delimiter="\t", encoding="utf-8"
        )
        print(records)
        self.assertTrue(len(records) > 0)

    def test_remove_items_with_certain_val_from_list(self):
        from sampytools.text_utils import remove_items_with_certain_val_from_list

        alist = ["one", "two", "three", ""]
        newlist = remove_items_with_certain_val_from_list(alist)
        print(newlist)
        self.assertTrue(len(newlist) == 3)

    def test_compare_two_files(self):
        from sampytools.text_utils import compare_two_files

        lines_one = [
            "The empire lasted for 1000 years",
            "The empire was great",
            "The empire started its long Fall",
        ]
        lines_two = [
            "The empire lasted for 1000 years",
            "The empire was great",
            "The empire started its centuries long Fall",
        ]
        file_one = self.test_folder / "test_file_one.txt"
        file_two = self.test_folder / "test_file_two.txt"
        file_one.write_text("\n".join(lines_one))
        file_two.write_text("\n".join(lines_two))
        diffres = compare_two_files(file_one, file_two)
        print(diffres.file1_vs_file2)
        print(diffres.intersection)
        self.assertTrue(len(diffres.file1_vs_file2) == 1)

    def test_save_lines_to_file(self):
        from sampytools.text_utils import save_lines_to_file
        line_one="portfolio_name,cusip,weight"
        line_two="ABC123,CUSIP00,0.5"
        folder=pathlib.Path.cwd()/"test_data"
        file="test_file.csv"
        save_lines_to_file(folder/file, [line_one,line_two], encoding="utf-8")
        df=pd.read_csv(folder/file)
        print(df.to_string())
        self.assertTrue("portfolio_name" in df.columns)

    def test_get_message_clusters(self):
        from sampytools.text_utils import get_message_clusters

        # Mock version of `get_common_common_part_of_message_across_documents`
        def mock_get_common_common_part_of_message_across_documents(msg, tokenizer, vec, features, topk):
            # Return the first token in message for simplicity
            tokens = tokenizer(msg)
            return tokens[0] if tokens else msg

        # Inject the mock function (you can patch it if needed)
        import sampytools.text_utils
        sampytools.text_utils.get_common_common_part_of_message_across_documents = mock_get_common_common_part_of_message_across_documents

        # Example messages with near-duplicates to ensure clustering
        messages = [
            "Error while reading file /data/abc.txt",
            "Error while reading file /data/xyz.txt",
            "Connection to database failed at port 5432",
            "Database connection failed on port 5432",
            "User login failed due to wrong credentials",
            "Login failed: invalid username or password"
        ]

        result = get_message_clusters(messages, n_components=3)

        clustered_messages = result['clustered_messages']
        tfidf_features = result['tfidf_features']
        tokenizer = result['tokenizer']
        nmf_features = result['nmf_feature']

        # Assertions
        self.assertIsInstance(clustered_messages, dict)
        self.assertGreaterEqual(len(clustered_messages), 2)
        self.assertTrue(all(msg in messages for msg in clustered_messages.keys()))
        self.assertTrue(hasattr(tokenizer, '__call__'))
        self.assertEqual(nmf_features.shape[0], len(messages))
        self.assertEqual(len(tfidf_features), result['tfidf'].idf_.shape[0])



if __name__ == "__main__":
    unittest.main()
