from Bio import Entrez,SeqIO
import csv

# 参数设置
Entrez.email = "example@163.com"
Entrez.tool = "exampleScript"

csv_file = ".\PATRIC_genome.csv"   # csv文件路径


def get_gbk(csv_file):
    """
    从csv文件中获取GenBank Accessions，返回基因组登记号列表（gbk_List）
    :param csv_file: csv文件
    :return: 含有所有GenBank Accessions的列表
    """
    gbk_list =[]  # 存储GenBank Accessions
    # 读取csv文件
    csv_flie = csv.reader(open(csv_file))

    # 确定“GenBank Accessions”所在位置（即索引）
    goal_index = 0
    for l in csv_flie:
        goal_index = l.index("GenBank Accessions")
        break
    # 读取所有组的信息找到对应的"GenBank Accessions"
    for line in csv_flie:
        gbk_list.append(line[goal_index])

    return gbk_list


def download_gbk(gbk_list,goal_path):
    """
    下载提供的基因组登记号列表中对应的genbank格式基因组序列，并存储到本地
    :param gbk_list: "GenBank Accessions"列表
    :param goal_path: gbk文件存储路径
    :return: failed_list
    """

    # 下载失败的基因组序列列表
    failed_list = []
    print("开始下载gbk格式基因组序列文件")
    for gbk_id in gbk_list:
        file_name = goal_path + gbk_id + ".gbk"  # 指明路径：以GenBank Accessions命名文件
        try:
            handle = Entrez.efetch(db="nucleotide",id=gbk_id,rettype="gb",retmode="text")
            file_handle=open(file_name,"w")
            file_handle.write(handle.read())
            file_handle.close()
            # handle.close()
            print("下载{}成功！".format(gbk_id))
        except:
            print("下载{}失败！！！".format(gbk_id))
            failed_list.append(gbk_id)
    return failed_list

def download_fasta(gbk_list,goal_path):
    """
    下载提供的基因组登记号列表中对应的fasta格式基因组序列，并存储到本地
    :param gbk_list: "GenBank Accessions"列表
    :param goal_path: fasta文件存储路径
    :return: failed_list
    """
    # 下载失败的基因组序列列表
    failed_list = []

    print("开始下载fasta格式基因组序列文件")
    for gbk_id in gbk_list:
        file_name = goal_path + gbk_id + ".fasta"  # 指明路径：以GenBank Accessions命名文件

        try:
            handle = Entrez.efetch(db="nucleotide", id=gbk_id, rettype="fasta", retmode="text")
            file_handle = open(file_name, "w")
            file_handle.write(handle.read())
            file_handle.close()
            # handle.close()
            print("下载{}成功！".format(gbk_id))
        except:
            print("下载{}失败！！！".format(gbk_id))
            failed_list.append(gbk_id)
    return failed_list


def try_again(failed_list,goal_path,rettype):
    """
    对下载失败的基因组序列再尝试下载一次,返回两次都下载失败的对应基因组登记号列表
    :param failed_list: 第一次下载失败的基因组序列列表
    :param goal_path: 目标路径
    :return: end_failed
    """
    end_failed = []
    for gbk_id in failed_list:
        if rettype == "gb":
            file_name = goal_path + gbk_id + ".gbk"  # 指明路径：以GenBank Accessions命名文件
        else:
            file_name = goal_path + gbk_id + "."+rettype
        try:
            handle = Entrez.efetch(db="nucleotide",id=gbk_id,rettype=rettype,retmode="text")
            file_handle=open(file_name,"w")
            file_handle.write(handle.read())
            file_handle.close()
            # handle.close()
            print("第二次下载{}成功！".format(file_name))
        except:
            print("{}下载失败！！，请手动下载！".format(file_name))
            end_failed.append(gbk_id)
    return end_failed


def main():
    # 获取基因组登记号列表
    gbk_list=get_gbk(csv_file)

    # 下载对应gbk格式基因组序列文件，并打印下载失败的登记号
    failed_gbkdown=download_gbk(gbk_list,".\\gbk_file\\")
    failed_gbklist=try_again(failed_gbkdown,".\\gbk_file\\","gb")
    print("需手动下载的基因组序列(gbk格式)：{}".format(failed_gbklist))

    # 下载对应fasta格式基因组序列文件，并打印下载失败的登记号
    failed_fastadown = download_fasta(gbk_list,".\\fasta_file\\")
    failed_fastalist = try_again(failed_fastadown,".\\fasta_file\\","fasta")
    print("需手动下载的基因组序列(fasta格式)：{}".format(failed_fastalist))


if __name__ == '__main__':
    main()

