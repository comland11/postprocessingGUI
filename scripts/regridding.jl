using LinearAlgebra
using DelimitedFiles
using PyCall


mat_data = py"self.mat_data"
nPoints = py"self.nPoints"

kCartesian = mat_data["kCartesian"]
k_space_raw = mat_data["kSpaceRaw"]

kxOriginal = real.(reshape(k_space_raw[:, 1], :))
kyOriginal = real.(reshape(k_space_raw[:, 2], :))
kzOriginal = real.(reshape(k_space_raw[:, 3], :))
kxTarget = reshape(kCartesian[:, 1], :)
kyTarget = reshape(kCartesian[:, 2], :)
kzTarget = reshape(kCartesian[:, 3], :)

valCartesian = griddata((kxOriginal, kyOriginal, kzOriginal), reshape(k_space_raw[:, 4], :),
                        (kxTarget, kyTarget, kzTarget), "linear", fill_value=0, rescale=false)

k_space = reshape(valCartesian, nPoints[3], nPoints[2], nPoints[1])

# Exporter les données vers un fichier .npy
np = pyimport("numpy")
np.save("self.k_space.npy", k_space)

