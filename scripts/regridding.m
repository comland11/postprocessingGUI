k_space_raw = reshape(kSpaceRaw(:, 4), 1, []);
kx_original = reshape(real(kSpaceRaw(:, 1)), 1, []);
ky_original = reshape(real(kSpaceRaw(:, 2)), 1, []);
kz_original = reshape(real(kSpaceRaw(:, 3)), 1, []);
kxTarget = reshape(kCartesian(:, 1), 1, []);
kyTarget = reshape(kCartesian(:, 2), 1, []);
kzTarget = reshape(kCartesian(:, 3), 1, []);

valCartesian = griddata(kx_original, ky_original, kz_original, k_space_raw ,kxTarget, kyTarget, kzTarget, "linear");
k_space = reshape(valCartesian, [nPoints(1), nPoints(2), nPoints(3)]);
k_space = permute(k_space, [3, 2, 1]);

% Save k_space in a .mat file
save('k_space.mat', 'k_space');

