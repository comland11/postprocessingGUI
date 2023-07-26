% Extract the 4th column of kSpaceRaw and reshape it into a 1D array
k_space_raw = reshape(kSpaceRaw(:, 4), 1, []);

% Extract and reshape the real parts of the first three columns of kSpaceRaw into 1D arrays
kx_original = reshape(real(kSpaceRaw(:, 1)), 1, []);
ky_original = reshape(real(kSpaceRaw(:, 2)), 1, []);
kz_original = reshape(real(kSpaceRaw(:, 3)), 1, []);

% Extract and reshape the first three columns of kCartesian into 1D arrays
kxTarget = reshape(kCartesian(:, 1), 1, []);
kyTarget = reshape(kCartesian(:, 2), 1, []);
kzTarget = reshape(kCartesian(:, 3), 1, []);

% Perform linear interpolation using griddata to create a new k_space grid
valCartesian = griddata(kx_original, ky_original, kz_original, k_space_raw, kxTarget, kyTarget, kzTarget, "linear");

% Reshape the interpolated k_space data into a 3D array
k_space = reshape(valCartesian, [nPoints(1), nPoints(2), nPoints(3)]);

% Permute the dimensions to match the desired order (assuming the target order is [z, y, x])
k_space = permute(k_space, [3, 2, 1]);

% Save 'k_space' in a .mat file
save('k_space.mat', 'k_space');


