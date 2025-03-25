# Secure-file-transfer-system
**End-to-End Secure File Transfer System Using AES and HMAC**

**INTODUCTION:**                                             
A Secure File Transfer System is a method of sharing files between devices or users while ensuring the confidentiality, integrity, and security of the data. It uses encryption techniques to protect the files during transfer, preventing unauthorized access or tampering. This System is designed to enable the safe exchange of files over a network by safeguarding against unauthorized access, tampering, and data breaches.
This system is widely used in scenarios where sensitive or critical data, such as personal information or business documents, needs to be shared safely over a network. Its goal is to provide a reliable and protected file-sharing process.
These systems are crucial in industries where sensitive data, such as financial records, medical information, or legal documents, is frequently transmitted. By ensuring both confidentiality and integrity secure file transfer systems protect data.


**OBJECTIVES:**                                                              
  Secure Data Upload and Retrieval               
  Ensure Data Integrity Using HMAC                      
  Enable Server-Side File Storage with Re-encryption                
  Provide Secure Authentication                   
  Minimize the Risk of Data Breach.


**PROPOSED SYSTEM:**                                                           
In the proposed file-sharing system, the process of uploading and downloading files is secured using AES encryption and HMAC (Hash-Based Message Authentication Code). When a client uploads a file, the file is first encrypted using AES to ensure confidentiality. The client then calculates an HMAC for the encrypted file using a shared secret key and sends both the encrypted file and the HMAC to the server. The server computes its own HMAC for the received file and compares it to the client's HMAC. If they match, the server re-encrypts the file and saves it for storage; otherwise, the upload is rejected. For downloading, when the client requests a file, the server retrieves the encrypted file, decrypts it, and computes a new HMAC. The client then calculates its own HMAC for the received file and compares it with the server's. If the HMACs match, the client decrypts the file to restore its original content; otherwise, it rejects the file and logs an error, ensuring file integrity and secure data transfer.

**ARCHITECTURE:**                                                         

**FILE UPLOAD:**                                                                          
![image](https://github.com/user-attachments/assets/a0a299f6-ccd0-448f-a86a-b12edc2a58ee)                                              
**FILE DOWNLOAD**                                                              
![image](https://github.com/user-attachments/assets/971224f5-fc30-48cb-907d-c037a26e067d)                                               




**RESULTS:**                                                                 
Before running the server and client programs, I have set up a directory structure. I have created a directory called server_files in the project folder. This is where the server will save uploaded files in encrypted format.
I have also created a file named testfile.txt in the client's directory. This file will be encrypted, sent to the server, and stored in server_files.
After starting the server by executing server.py, It will initialize and listen for incoming client requests at http://127.0.0.1:5000.
After executing client.py to upload testfile.txt to the server.
The client successfully sent the file along with the computed HMAC.
The server received the file, verified its integrity (by comparing its own computed HMAC with the one sent by the client), and encrypted the file before saving it.
The server sent a success response to the client.
The client requested the file from the server. The server retrieved the encrypted file from server_files then decrypted it to its original state and sent the file and a new HMAC to the client.
The client verified the file's integrity by comparing the received HMAC with its own computed HMAC. 
The file was saved locally as downloaded_testfile.txt.
After executing the programs the original file (testfile.txt) is securely stored in encrypted form in the server's server_files directory. 
The client successfully downloaded and verified the file, saving it as downloaded_testfile.txt.

**CONCLUSION:**                                                             
In conclusion, this project successfully demonstrates a secure file transfer system that ensures both the confidentiality and integrity of user files. By incorporating AES encryption, files are protected from unauthorized access during transit and storage. The use of HMAC verification guarantees that the files remain untampered throughout the process, providing a reliable mechanism to detect any integrity issues. The system enhances traditional client-server architecture by adding robust cryptographic techniques, making it a practical solution for secure file management. This project highlights the importance of combining encryption and integrity checks to build trust and security in modern file-sharing applications.






