import json
import numpy as np

#先创建一个坐标系的类，方便管理
class CoordinateSystem:
    def __init__(self, basis, vectors_abs, dtype=np.float64):
        self.dtype = dtype
        self.basis = np.array(basis, dtype=dtype).T           # 将输入的行向量基矩阵转置为列向量形式，以适配程序的矩阵运算
        vectors_abs = np.array(vectors_abs, dtype=dtype)
        self.dim = self.basis.shape[0]
        self.N = vectors_abs.shape[0]

        # 检查基底是否线性无关
        if np.linalg.matrix_rank(self.basis) != self.dim:
            raise ValueError("初始基矩阵线性相关，不能构成坐标系")

        # 初始时，根据绝对坐标和初始基，计算向量在当前基各轴上的投影长度
        # 要算投影直接用高中的投影公式就好了，但是要换成矩阵来乘
        axis_norms = np.linalg.norm(self.basis, axis=0)
        dot = np.abs(vectors_abs @ self.basis)
        self.proj_lengths = dot / axis_norms

    # 应对change_axis这个task
    # 将当前坐标系下的向量（用投影长度表示）转移到新基下，要输入data文件中的new basis
    def change_basis(self, new_basis):
        new_basis = np.array(new_basis, dtype=self.dtype).T # 同样将输入的行向量基矩阵转置为列向量形式

        # 先检查一下新基地数据有没有出错
        if new_basis.shape != (self.dim, self.dim):
            raise ValueError("新基维度与当前坐标系维度不匹配")
        if np.linalg.matrix_rank(new_basis) != self.dim:
            raise ValueError("新基矩阵线性相关，不能构成坐标系")

        # 根据当前投影长度和当前基，恢复绝对坐标
        current_axis_norms = np.linalg.norm(self.basis, axis=0)
        unit_dirs = self.basis / current_axis_norms
        v_abs = self.proj_lengths @ unit_dirs.T

        # 计算新基下各轴上的投影长度
        new_axis_norms = np.linalg.norm(new_basis, axis=0)
        dot = np.abs(v_abs @ new_basis)
        self.proj_lengths = dot / new_axis_norms
        self.basis = new_basis

    # 返回当前坐标系下每个向量在各轴上的投影长度，应对axis_projection
    def projection(self):
        return self.proj_lengths

    # 应对axis_angle，计算当前坐标系下每个向量与每个轴的夹角 结果表示为弧度
    def angle(self):
        # 1.算绝对坐标
        current_axis_norms = np.linalg.norm(self.basis, axis=0)
        unit_dirs = self.basis / current_axis_norms
        v_abs = self.proj_lengths @ unit_dirs.T

        # 2.计算向量模长和基向量模长
        vec_norms = np.linalg.norm(v_abs, axis=1, keepdims=True)
        axis_norms = current_axis_norms

        # 3.计算点乘的结果
        dot = v_abs @ self.basis

        # 4.计算余弦，避免除零
        cos_theta = np.full_like(dot, np.nan, dtype=self.dtype)
        nonzero_mask = (vec_norms != 0).flatten()
        if np.any(nonzero_mask):
            dot_nonzero = dot[nonzero_mask]
            vec_norms_nonzero = vec_norms[nonzero_mask]
            denom = vec_norms_nonzero * axis_norms
            cos_theta[nonzero_mask] = dot_nonzero / denom
        cos_theta = np.clip(cos_theta, -1, 1)
        theta = np.arccos(cos_theta)
        return theta

    # 应对area
    def area_scale(self):
        """
        当前基张成的平行多面体体积（即面积缩放倍数）。
        """
        return abs(np.linalg.det(self.basis))

def main():
    np.set_printoptions(suppress=True, precision=6, floatmode='fixed')  # 设置np
    with open('data.json', 'r', encoding='utf-8') as f:                 # 导入json，文件夹中的data1.json是任务文档中的示例数据
        data = json.load(f)
    for group in data:
        print(f"\n{group['group_name']}")
        try:
            cs = CoordinateSystem(group['ori_axis'], group['vectors'])
        except ValueError as e:
            print(f"初始化坐标系失败: {e}")
            continue

        count=0     #用于计数
        for task in group['tasks']:
            count+=1
            tasktype = task['type']
            if tasktype == 'axis_projection':  # 用if elif识别各个任务，分别执行
                proj = cs.projection()
                print(f"\n任务{count}: 投影长度")
                print(proj)
            elif tasktype == 'axis_angle':
                ang = cs.angle()
                print(f"\n任务{count}: 夹角")
                print(ang)
            elif tasktype == 'area':
                area = cs.area_scale()
                print(f"\n任务{count}: 面积缩放")
                print(f"面积缩放倍数: {area:.6f}")
            elif tasktype == 'change_axis':
                new_basis = task['obj_axis']
                print(f"\n任务{count}: 坐标系转移")
                try:
                    cs.change_basis(new_basis)
                    # 输出转移后的向量表示（投影长度）
                    # 说明：由于对线性变换掌握还不熟练，这里用投影来计算向量的新坐标
                    print(cs.proj_lengths)
                except ValueError as e:
                    print(f"错误:{e}")
            else:
                print("未知任务类型")

if __name__ == '__main__':
    main()