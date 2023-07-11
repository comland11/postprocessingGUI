function k_space = getKSpace()
    kCartesian = mat_data.kCartesian;
    k_space_raw = mat_data.kSpaceRaw;

    kxOriginal = reshape(real(k_space_raw(:, 1)), 1, []);
    kyOriginal = reshape(real(k_space_raw(:, 2)), 1, []);
    kzOriginal = reshape(real(k_space_raw(:, 3)), 1, []);
    kxTarget = reshape(kCartesian(:, 1), 1, []);
    kyTarget = reshape(kCartesian(:, 2), 1, []);
    kzTarget = reshape(kCartesian(:, 3), 1, []);
    valCartesian = griddata([kxOriginal; kyOriginal; kzOriginal], reshape(k_space_raw(:, 4), 1, []), ...
                            [kxTarget; kyTarget; kzTarget], "linear", 0);
    k_space = reshape(valCartesian, [nPoints(3), nPoints(2), nPoints(1)]);
end

k_space = getKSpace();

