# CredibilityDataset
Considerations and details about the dataset:
- In the inlink_list all of the documents contain claims.
- Outlinked documents may or may not contain claims.
- isClaim: The possible fields are "claim", "document", "claim and document".
- labelScale: if the label scale is set as plain text it means that the labels of this seed is a plaintext
- Labels: removed extra spaces, breaklines, transformed everything to lower case. This happened to the following seeds (fai,fay, fut, thl)
- to parse the pdf we extract the text using pypdf4 and then use wordninja library to split text into tokens

